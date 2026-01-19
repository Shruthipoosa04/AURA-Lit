# timeline_builder.py
from collections import defaultdict

def build_timeline(papers):
    timeline = defaultdict(list)
    for p in papers:
        timeline[p["year"]].append(p["title"])
    return dict(sorted(timeline.items(), reverse=True))
