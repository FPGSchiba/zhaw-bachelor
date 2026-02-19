import json
from requests_sse import EventSource

last_id = None
url = "https://stream.wikimedia.org/v2/stream/recentchange"

headers = {
    "User-Agent": "MyBigDataProject/1.0 (your@email.com)"
}

with EventSource(url, headers=headers) as stream:
    for event in stream:
        if event.type == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                # discard canary events
                if change['meta']['domain'] == 'canary':
                    continue
                print(change)
