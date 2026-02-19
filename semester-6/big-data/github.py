"""
GitHub Events API Explorer
---------------------------
Polls the GitHub public events API and gives a live overview
of what kind of events are happening across all public repositories.

Usage:
    pip install requests rich
    python github_events_explorer.py

Optional: Set a GitHub token to get a higher rate limit (5000 req/h vs 60 req/h):
    export GITHUB_TOKEN=your_token_here
"""

import os
import time
import requests
from collections import defaultdict, deque
from datetime import datetime

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
    print("Tip: install 'rich' for a prettier output: pip install rich")

# ── Config ────────────────────────────────────────────────────────────────────
POLL_INTERVAL_SECONDS = 10   # GitHub updates the feed roughly every 10s
MAX_PAGES             = 3    # Pages to fetch per poll (each page = 30 events)
HISTORY_SIZE          = 500  # How many events to keep in memory

GITHUB_API_URL = "https://api.github.com/events"
TOKEN          = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept":     "application/vnd.github+json",
    "User-Agent": "ZHAW-BigData-Explorer/1.0",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

# ── Event type metadata ───────────────────────────────────────────────────────
EVENT_META = {
    "PushEvent":                  ("📦", "Push",              "Commits pushed to a branch"),
    "PullRequestEvent":           ("🔀", "Pull Request",      "PR opened, closed, or merged"),
    "IssuesEvent":                ("🐛", "Issue",             "Issue opened, closed, or labeled"),
    "WatchEvent":                 ("⭐", "Star",              "Repository starred"),
    "ForkEvent":                  ("🍴", "Fork",              "Repository forked"),
    "CreateEvent":                ("🌱", "Create",            "Branch, tag, or repo created"),
    "DeleteEvent":                ("🗑️",  "Delete",            "Branch or tag deleted"),
    "IssueCommentEvent":          ("💬", "Issue Comment",     "Comment on an issue or PR"),
    "PullRequestReviewEvent":     ("👀", "PR Review",         "Pull request reviewed"),
    "PullRequestReviewCommentEvent": ("🗨️", "PR Review Comment", "Comment on a PR diff"),
    "ReleaseEvent":               ("🚀", "Release",           "New release published"),
    "PublicEvent":                ("🔓", "Made Public",       "Private repo made public"),
    "MemberEvent":                ("👤", "Member",            "Collaborator added/removed"),
    "GollumEvent":                ("📝", "Wiki",              "Wiki page created/updated"),
    "CommitCommentEvent":         ("📌", "Commit Comment",    "Comment on a commit"),
}

# ── State ─────────────────────────────────────────────────────────────────────
seen_ids       = set()
event_counts   = defaultdict(int)
recent_events  = deque(maxlen=HISTORY_SIZE)
language_counts = defaultdict(int)
total_fetched  = 0
poll_count     = 0
last_etag      = None

console = Console() if RICH_AVAILABLE else None


def fetch_events():
    """Fetch new events from the GitHub API, respecting ETags to avoid wasted calls."""
    global last_etag, total_fetched

    new_events = []
    etag_header = {"If-None-Match": last_etag} if last_etag else {}

    for page in range(1, MAX_PAGES + 1):
        try:
            resp = requests.get(
                GITHUB_API_URL,
                headers={**HEADERS, **etag_header},
                params={"per_page": 30, "page": page},
                timeout=10,
            )

            if resp.status_code == 304:
                # Not modified — no new events since last poll
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
    """Extract and aggregate useful info from a single event."""
    etype = event.get("type", "Unknown")
    event_counts[etype] += 1

    repo  = event.get("repo", {}).get("name", "?")
    actor = event.get("actor", {}).get("login", "?")
    ts    = event.get("created_at", "")[:19].replace("T", " ")

    # Extract language from PushEvent payload if present
    lang  = event.get("payload", {}).get("commits", [{}])
    # (language not in events directly; would need repo API call — skip for now)

    # Build a human-readable detail line
    payload = event.get("payload", {})
    detail  = ""
    if etype == "PushEvent":
        n = len(payload.get("commits", []))
        detail = f"{n} commit(s)"
    elif etype in ("PullRequestEvent", "IssuesEvent"):
        detail = payload.get("action", "")
    elif etype == "CreateEvent":
        detail = f"{payload.get('ref_type', '')} '{payload.get('ref', '')}'"
    elif etype == "WatchEvent":
        detail = payload.get("action", "starred")
    elif etype == "ReleaseEvent":
        tag = payload.get("release", {}).get("tag_name", "")
        detail = f"tag {tag}"

    recent_events.appendleft({
        "type":   etype,
        "repo":   repo,
        "actor":  actor,
        "time":   ts,
        "detail": detail,
    })


def make_summary_table():
    """Build a rich table of event type counts."""
    table = Table(title="📊 Event Type Breakdown", box=box.ROUNDED, show_lines=False)
    table.add_column("Icon", justify="center", no_wrap=True)
    table.add_column("Event Type",  style="cyan",    min_width=22)
    table.add_column("Count",       justify="right",  style="bold yellow")
    table.add_column("Share",       justify="right")
    table.add_column("Description", style="dim")

    total = sum(event_counts.values()) or 1
    sorted_events = sorted(event_counts.items(), key=lambda x: -x[1])

    for etype, count in sorted_events:
        icon, label, desc = EVENT_META.get(etype, ("❓", etype, ""))
        pct = f"{count / total * 100:.1f}%"
        bar = "█" * int(count / total * 20)
        table.add_row(icon, label, str(count), f"{pct} {bar}", desc)

    return table


def make_recent_table():
    """Build a rich table of the most recent events."""
    table = Table(title="🕐 Most Recent Events (last 15)", box=box.SIMPLE)
    table.add_column("Time",        style="dim",    no_wrap=True)
    table.add_column("Type",        style="cyan",   min_width=18)
    table.add_column("Actor",       style="green",  min_width=14)
    table.add_column("Repository",  style="white",  min_width=28)
    table.add_column("Detail",      style="dim")

    for ev in list(recent_events)[:15]:
        icon, label, _ = EVENT_META.get(ev["type"], ("❓", ev["type"], ""))
        table.add_row(
            ev["time"],
            f"{icon} {label}",
            ev["actor"],
            ev["repo"],
            ev["detail"],
        )
    return table


def print_plain(new_events):
    """Fallback output when rich is not installed."""
    for ev in new_events:
        etype = ev.get("type", "?")
        repo  = ev.get("repo", {}).get("name", "?")
        actor = ev.get("actor", {}).get("login", "?")
        print(f"  [{etype}] {actor} → {repo}")

    print("\n--- Event Counts So Far ---")
    for etype, count in sorted(event_counts.items(), key=lambda x: -x[1]):
        icon, label, _ = EVENT_META.get(etype, ("?", etype, ""))
        print(f"  {icon}  {label:<28} {count}")
    print()


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    global poll_count

    print("🔍 GitHub Events Explorer — connecting to GitHub API...")
    if TOKEN:
        print("✅ Using authenticated requests (5000 req/h limit)")
    else:
        print("⚠️  No GITHUB_TOKEN set — using unauthenticated (60 req/h limit)")
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
                    f"New this poll: [yellow]{len(new_events)}[/yellow] | "
                    f"Total seen: [yellow]{total_fetched}[/yellow] | "
                    f"Unique types: [cyan]{len(event_counts)}[/cyan] | "
                    f"[dim]{datetime.now().strftime('%H:%M:%S')}[/dim]"
                )

                live.update(Panel(
                    Columns([make_summary_table(), make_recent_table()]),
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
        print("\n\n👋 Stopped. Final event counts:")
        for etype, count in sorted(event_counts.items(), key=lambda x: -x[1]):
            icon, label, _ = EVENT_META.get(etype, ("?", etype, ""))
            print(f"  {icon}  {label:<28} {count}")