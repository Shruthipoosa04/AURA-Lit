def fetch_papers(query, limit=5):
    papers = []

    # -------- Semantic Scholar (Primary) -------- #
    try:
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

        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json().get("data", [])

        for p in data:
            papers.append({
                "title": p.get("title", "N/A"),
                "authors": ", ".join([a["name"] for a in p.get("authors", [])[:3]]),
                "year": p.get("year", "N/A"),
                "abstract": p.get("abstract", ""),
                "link": p.get("url", "#")
            })

        if papers:
            return papers

    except:
        pass

    # -------- arXiv (Fallback – ALWAYS WORKS) -------- #
    try:
        import feedparser

        search_query = f"search_query=all:{query.replace(' ', '+')}&start=0&max_results={limit}"
        feed_url = f"http://export.arxiv.org/api/query?{search_query}"
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            papers.append({
                "title": entry.title,
                "authors": ", ".join([a.name for a in entry.authors[:3]]),
                "year": entry.published[:4],
                "abstract": entry.summary[:400],
                "link": entry.link
            })

    except:
        pass

    return papers
