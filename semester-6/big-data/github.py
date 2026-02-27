"""
GitHub Events API Explorer
---------------------------
Polls the GitHub public events API and gives a live overview
of what kind of events are happening across all public repositories.

Enriches each actor with geographic & profile data:
  • Location string  (GitHub profile)
  • Country + flag   (Nominatim geocoding)
  • Timezone         (timezonefinder from lat/lng)
  • Company          (GitHub profile)
  • Public repos     (GitHub profile)

The left panel shows a live Geo Distribution breakdown (by country)
instead of raw event types.

Usage:
    pip install requests rich timezonefinder
    python github_events_explorer.py

Optional: Set a GitHub token for a higher rate limit (5000 req/h vs 60 req/h):
    export GITHUB_TOKEN=your_token_here
"""

import os
import time
import requests
from collections import defaultdict, deque
from datetime import datetime

try:
    from timezonefinder import TimezoneFinder
    TF = TimezoneFinder()
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("Tip: pip install timezonefinder  for timezone resolution")

try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.columns import Columns
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Tip: pip install rich  for a prettier output")

# ── Config ────────────────────────────────────────────────────────────────────
POLL_INTERVAL_SECONDS = 10
MAX_PAGES             = 3
HISTORY_SIZE          = 500

GITHUB_API_URL = "https://api.github.com/events"
NOMINATIM_URL  = "https://nominatim.openstreetmap.org/search"
TOKEN          = os.getenv("GITHUB_TOKEN")

GITHUB_HEADERS = {
    "Accept":     "application/vnd.github+json",
    "User-Agent": "ZHAW-BigData-Explorer/1.0",
}
if TOKEN:
    GITHUB_HEADERS["Authorization"] = f"Bearer {TOKEN}"

# Nominatim requires a descriptive User-Agent per their usage policy
NOMINATIM_HEADERS = {
    "User-Agent":      "ZHAW-BigData-Explorer/1.0 (educational project)",
    "Accept-Language": "en",
}

# ── Event type metadata ───────────────────────────────────────────────────────
EVENT_META = {
    "PushEvent":                     ("📦", "Push",               "Commits pushed to a branch"),
    "PullRequestEvent":              ("🔀", "Pull Request",       "PR opened, closed, or merged"),
    "IssuesEvent":                   ("🐛", "Issue",              "Issue opened, closed, or labeled"),
    "WatchEvent":                    ("⭐", "Star",               "Repository starred"),
    "ForkEvent":                     ("🍴", "Fork",               "Repository forked"),
    "CreateEvent":                   ("🌱", "Create",             "Branch, tag, or repo created"),
    "DeleteEvent":                   ("🗑️",  "Delete",             "Branch or tag deleted"),
    "IssueCommentEvent":             ("💬", "Issue Comment",      "Comment on an issue or PR"),
    "PullRequestReviewEvent":        ("👀", "PR Review",          "Pull request reviewed"),
    "PullRequestReviewCommentEvent": ("🗨️", "PR Review Comment",  "Comment on a PR diff"),
    "ReleaseEvent":                  ("🚀", "Release",            "New release published"),
    "PublicEvent":                   ("🔓", "Made Public",        "Private repo made public"),
    "MemberEvent":                   ("👤", "Member",             "Collaborator added/removed"),
    "GollumEvent":                   ("📝", "Wiki",               "Wiki page created/updated"),
    "CommitCommentEvent":            ("📌", "Commit Comment",     "Comment on a commit"),
}

# ── Country flag emoji helper (ISO 3166-1 alpha-2 → Unicode flag) ─────────────
def country_flag(code: str) -> str:
    if not code or len(code) != 2:
        return "🌐"
    return chr(ord(code[0]) + 127397) + chr(ord(code[1]) + 127397)

# ── Caches ────────────────────────────────────────────────────────────────────
# username → full enriched profile dict
user_profile_cache: dict[str, dict] = {}
# raw location string → geocode result dict
geocode_cache: dict[str, dict] = {}

# ── State ─────────────────────────────────────────────────────────────────────
seen_ids       = set()
event_counts   = defaultdict(int)
country_counts = defaultdict(int)
recent_events  = deque(maxlen=HISTORY_SIZE)
total_fetched  = 0
poll_count     = 0
last_etag      = None

console = Console() if RICH_AVAILABLE else None


# ── Geo enrichment helpers ────────────────────────────────────────────────────

def geocode_location(location_str: str) -> dict:
    """
    Convert a free-text location string to country + coordinates via Nominatim.
    Returns dict with: country, country_code, lat, lng.
    Cached + throttled to respect Nominatim's 1 req/s policy.
    """
    if not location_str:
        return {"country": None, "country_code": None, "lat": None, "lng": None}

    key = location_str.lower().strip()
    if key in geocode_cache:
        return geocode_cache[key]

    result = {"country": None, "country_code": None, "lat": None, "lng": None}
    try:
        resp = requests.get(
            NOMINATIM_URL,
            headers=NOMINATIM_HEADERS,
            params={
                "q":              location_str,
                "format":         "json",
                "limit":          1,
                "addressdetails": 1,
            },
            timeout=8,
        )
        if resp.status_code == 200:
            hits = resp.json()
            if hits:
                hit     = hits[0]
                address = hit.get("address", {})
                result["country"]      = address.get("country")
                result["country_code"] = (address.get("country_code") or "").upper()
                result["lat"]          = float(hit.get("lat", 0))
                result["lng"]          = float(hit.get("lon", 0))
    except requests.RequestException:
        pass

    geocode_cache[key] = result
    time.sleep(1.1)   # Nominatim usage policy: max 1 request/second
    return result


def resolve_timezone(lat: float | None, lng: float | None) -> str | None:
    """Return IANA timezone name for given coordinates."""
    if not TF_AVAILABLE or lat is None or lng is None:
        return None
    try:
        return TF.timezone_at(lat=lat, lng=lng)
    except Exception:
        return None


def fetch_user_profile(username: str) -> dict:
    """
    Fetch GitHub public profile and enrich with geocoded location data.
    Result is cached per username.
    """
    if username in user_profile_cache:
        return user_profile_cache[username]

    profile = {
        "location":     None,
        "company":      None,
        "public_repos": None,
        "country":      None,
        "country_code": None,
        "timezone":     None,
        "lat":          None,
        "lng":          None,
    }

    try:
        resp = requests.get(
            f"https://api.github.com/users/{username}",
            headers=GITHUB_HEADERS,
            timeout=8,
        )
        if resp.status_code == 200:
            data = resp.json()
            profile["location"]     = data.get("location") or None
            profile["company"]      = (data.get("company") or "").strip("@ ").strip() or None
            profile["public_repos"] = data.get("public_repos")
    except requests.RequestException:
        pass

    # Geocode location → country + coordinates → timezone
    if profile["location"]:
        geo = geocode_location(profile["location"])
        profile["country"]      = geo["country"]
        profile["country_code"] = geo["country_code"]
        profile["lat"]          = geo["lat"]
        profile["lng"]          = geo["lng"]
        profile["timezone"]     = resolve_timezone(geo["lat"], geo["lng"])

    user_profile_cache[username] = profile
    return profile


# ── GitHub event fetching ─────────────────────────────────────────────────────

def fetch_events():
    """Fetch new events from the GitHub API, respecting ETags."""
    global last_etag, total_fetched

    new_events  = []
    etag_header = {"If-None-Match": last_etag} if last_etag else {}

    for page in range(1, MAX_PAGES + 1):
        try:
            resp = requests.get(
                GITHUB_API_URL,
                headers={**GITHUB_HEADERS, **etag_header},
                params={"per_page": 30, "page": page},
                timeout=10,
            )

            if resp.status_code == 304:
                break

            if resp.status_code == 403:
                reset = resp.headers.get("X-RateLimit-Reset", "?")
                print(f"⚠️  Rate limited. Resets at {reset}. Set GITHUB_TOKEN for higher limits.")
                break

            resp.raise_for_status()

            if page == 1:
                last_etag = resp.headers.get("ETag")

            for event in resp.json():
                if event["id"] not in seen_ids:
                    seen_ids.add(event["id"])
                    new_events.append(event)
                    total_fetched += 1

        except requests.RequestException as e:
            print(f"  Request error: {e}")
            break

    return new_events


def process_event(event):
    """Extract and aggregate info from one event, enriching with geo data."""
    etype = event.get("type", "Unknown")
    event_counts[etype] += 1

    repo  = event.get("repo",  {}).get("name",  "?")
    actor = event.get("actor", {}).get("login", "?")
    ts    = event.get("created_at", "")[:19].replace("T", " ")

    profile = fetch_user_profile(actor)

    country_key = profile["country"] or "Unknown"
    country_counts[country_key] += 1

    # Build detail string
    payload = event.get("payload", {})
    detail  = ""
    if etype == "PushEvent":
        n      = len(payload.get("commits", []))
        detail = f"{n} commit(s)"
    elif etype in ("PullRequestEvent", "IssuesEvent"):
        detail = payload.get("action", "")
    elif etype == "CreateEvent":
        detail = f"{payload.get('ref_type', '')} '{payload.get('ref', '')}'"
    elif etype == "WatchEvent":
        detail = payload.get("action", "starred")
    elif etype == "ReleaseEvent":
        tag    = payload.get("release", {}).get("tag_name", "")
        detail = f"tag {tag}"

    recent_events.appendleft({
        "type":         etype,
        "repo":         repo,
        "actor":        actor,
        "time":         ts,
        "detail":       detail,
        "location":     profile["location"]     or "—",
        "country":      profile["country"]      or "—",
        "country_code": profile["country_code"] or "",
        "timezone":     profile["timezone"]     or "—",
        "company":      profile["company"]      or "—",
        "public_repos": profile["public_repos"],
    })


# ── Rich display tables ───────────────────────────────────────────────────────

def make_geo_table():
    """Live country distribution (replaces the old event-type breakdown)."""
    table = Table(title="🌍 Geo Distribution (by Country)", box=box.ROUNDED, show_lines=False)
    table.add_column("",        justify="center", no_wrap=True, width=3)
    table.add_column("Country", style="cyan",     min_width=20)
    table.add_column("Events",  justify="right",  style="bold yellow")
    table.add_column("Share",   justify="right")

    total = sum(country_counts.values()) or 1
    top   = sorted(country_counts.items(), key=lambda x: -x[1])[:20]

    for country_name, count in top:
        # Look up country code from any matching cached profile
        code = ""
        for p in user_profile_cache.values():
            if p.get("country") == country_name and p.get("country_code"):
                code = p["country_code"]
                break

        flag    = country_flag(code)
        pct     = f"{count / total * 100:.1f}%"
        bar     = "█" * max(1, int(count / total * 16))
        display = country_name if country_name != "Unknown" else "[dim]Unknown[/dim]"
        table.add_row(flag, display, str(count), f"{pct} {bar}")

    return table


def make_recent_table():
    """Recent events enriched with country, timezone, company, and repo count."""
    table = Table(title="🕐 Most Recent Events (last 15)", box=box.SIMPLE)
    table.add_column("Time",     style="dim",     no_wrap=True)
    table.add_column("Type",     style="cyan",    min_width=16)
    table.add_column("Actor",    style="green",   min_width=14)
    table.add_column("Country",  style="magenta", min_width=14)
    table.add_column("Timezone", style="yellow",  min_width=18)
    table.add_column("Company",  style="blue",    min_width=12)
    table.add_column("Repos",    justify="right", style="dim",   min_width=5)
    table.add_column("Repo",     style="white",   min_width=24)
    table.add_column("Detail",   style="dim")

    for ev in list(recent_events)[:15]:
        icon, label, _ = EVENT_META.get(ev["type"], ("❓", ev["type"], ""))

        flag    = country_flag(ev["country_code"])
        country = ev["country"] if ev["country"] != "—" else "[dim]unknown[/dim]"
        tz      = ev["timezone"] if ev["timezone"] != "—" else "[dim]—[/dim]"
        company = ev["company"]  if ev["company"]  != "—" else "[dim]—[/dim]"
        repos   = str(ev["public_repos"]) if ev["public_repos"] is not None else "[dim]?[/dim]"

        table.add_row(
            ev["time"],
            f"{icon} {label}",
            ev["actor"],
            f"{flag} {country}",
            tz,
            company,
            repos,
            ev["repo"],
            ev["detail"],
        )
    return table


def print_plain(new_events):
    """Fallback plain-text output when rich is not installed."""
    for ev in new_events:
        actor   = ev.get("actor", {}).get("login", "?")
        etype   = ev.get("type",  "?")
        repo    = ev.get("repo",  {}).get("name", "?")
        p       = fetch_user_profile(actor)
        country = p["country"]  or "unknown country"
        tz      = p["timezone"] or "unknown tz"
        company = p["company"]  or "—"
        print(f"  [{etype}] {actor} @ {company} | {country} ({tz}) → {repo}")

    print("\n--- Country Breakdown ---")
    for country_name, count in sorted(country_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {country_name:<30} {count}")
    print()


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    global poll_count

    print("🔍 GitHub Events Explorer — connecting to GitHub API...")
    if TOKEN:
        print("✅ Using authenticated requests (5000 req/h limit)")
    else:
        print("⚠️  No GITHUB_TOKEN set — unauthenticated limit is 60 req/h")
    if TF_AVAILABLE:
        print("🌐 Timezone resolution: enabled (timezonefinder)")
    else:
        print("⚠️  Timezone resolution: disabled — pip install timezonefinder")
    print(f"   Polling every {POLL_INTERVAL_SECONDS}s | Ctrl+C to stop\n")

    if RICH_AVAILABLE:
        with Live(console=console, refresh_per_second=1, screen=False) as live:
            while True:
                poll_count += 1
                new_events = fetch_events()
                for ev in new_events:
                    process_event(ev)

                status = (
                    f"[bold]Poll #{poll_count}[/bold] | "
                    f"New: [yellow]{len(new_events)}[/yellow] | "
                    f"Total: [yellow]{total_fetched}[/yellow] | "
                    f"Countries: [cyan]{len(country_counts)}[/cyan] | "
                    f"Users resolved: [cyan]{len(user_profile_cache)}[/cyan] | "
                    f"[dim]{datetime.now().strftime('%H:%M:%S')}[/dim]"
                )

                live.update(Panel(
                    Columns([make_geo_table(), make_recent_table()]),
                    title=status,
                    border_style="blue",
                ))

                time.sleep(POLL_INTERVAL_SECONDS)
    else:
        while True:
            poll_count += 1
            new_events = fetch_events()
            for ev in new_events:
                process_event(ev)
            print(f"\n=== Poll #{poll_count} | +{len(new_events)} new | Total: {total_fetched} ===")
            print_plain(new_events)
            time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Stopped.")
        print(f"   Users resolved:     {len(user_profile_cache)}")
        print(f"   Locations geocoded: {len(geocode_cache)}")
        print("\nTop countries:")
        for country_name, count in sorted(country_counts.items(), key=lambda x: -x[1])[:10]:
            code = ""
            for p in user_profile_cache.values():
                if p.get("country") == country_name and p.get("country_code"):
                    code = p["country_code"]
                    break
            flag = country_flag(code)
            print(f"  {flag}  {country_name:<30} {count}")