import requests
import time
from datetime import datetime
import feedparser

def fetch_papers(query, limit=15, years_back=10):
    papers = []
    seen_titles = set()

    current_year = datetime.now().year
    start_year = current_year - years_back

    # ---------- Semantic Scholar (with retry) ---------- #
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {
        "User-Agent": "AURA-Lit-Research-Agent/1.0",
        "Accept": "application/json"
    }
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,abstract,url"
    }

    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json().get("data", [])
                for p in data:
                    year = p.get("year")
                    title = p.get("title")
                    if (
                        title
                        and title not in seen_titles
                        and year
                        and start_year <= year <= current_year
                    ):
                        seen_titles.add(title)
                        papers.append({
                            "title": title,
                            "authors": ", ".join([a["name"] for a in p.get("authors", [])[:3]]),
                            "year": year,
                            "abstract": p.get("abstract", ""),
                            "link": p.get("url", "#"),
                            "source": "Semantic Scholar"
                        })
                break
        except:
            time.sleep(2)

    # ---------- arXiv (always attempted) ---------- #
    try:
        search_query = f"search_query=all:{query.replace(' ', '+')}&start=0&max_results={limit*2}"
        feed_url = f"http://export.arxiv.org/api/query?{search_query}"
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            year = int(entry.published[:4])
            title = entry.title

            if (
                title not in seen_titles
                and start_year <= year <= current_year
            ):
                seen_titles.add(title)
                papers.append({
                    "title": title,
                    "authors": ", ".join([a.name for a in entry.authors[:3]]),
                    "year": year,
                    "abstract": entry.summary[:500],
                    "link": entry.link,
                    "source": "arXiv"
                })
    except:
        pass

    return papers[:limit]
