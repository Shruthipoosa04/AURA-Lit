import requests
import time
from datetime import datetime
import feedparser


def clean_text(text):
    if not text:
        return ""
    return str(text).replace("\n", " ").strip()


def fetch_papers(query, limit=25, start_year=2000):

    papers = []
    seen_titles = set()
    current_year = datetime.now().year

    # -------------------- Semantic Scholar -------------------- #
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    headers = {
        "User-Agent": "AURA-Lit-Agent",
        "Accept": "application/json"
    }

    offset = 0
    batch_size = 100

    while len(papers) < limit:

        params = {
            "query": query,
            "limit": batch_size,
            "offset": offset,
            "fields": "title,authors,year,abstract,url"
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code != 200:
                break

            data = response.json().get("data", [])
            if not data:
                break

            for p in data:

                title = p.get("title")
                year = p.get("year")

                if not title or not year:
                    continue

                if title in seen_titles:
                    continue

                if not (start_year <= year <= current_year):
                    continue

                seen_titles.add(title)

                papers.append({
                    "title": title,
                    "authors": ", ".join(
                        [a["name"] for a in p.get("authors", [])[:3]]
                    ),
                    "year": year,
                    "abstract": clean_text(p.get("abstract")),
                    "link": p.get("url", "#"),
                    "source": "Semantic Scholar"
                })

                if len(papers) >= limit:
                    break

            offset += batch_size

        except Exception:
            break

    # -------------------- arXiv Fallback -------------------- #
    if len(papers) < limit:

        remaining = limit - len(papers)

        try:
            search_query = f"search_query=all:{query.replace(' ', '+')}&start=0&max_results={remaining*3}"
            feed_url = f"http://export.arxiv.org/api/query?{search_query}"

            feed = feedparser.parse(feed_url)

            for entry in feed.entries:

                year = int(entry.published[:4])
                title = entry.title.strip()

                if title in seen_titles:
                    continue

                if not (start_year <= year <= current_year):
                    continue

                seen_titles.add(title)

                abstract = clean_text(getattr(entry, "summary", ""))

                papers.append({
                    "title": title,
                    "authors": ", ".join(
                        [a.name for a in entry.authors[:3]]
                    ),
                    "year": year,
                    "abstract": abstract,
                    "link": entry.link,
                    "source": "arXiv"
                })

                if len(papers) >= limit:
                    break

        except Exception:
            pass

    # -------------------- Final Sort -------------------- #
    papers = sorted(papers, key=lambda x: x["year"])

    return papers[:limit]