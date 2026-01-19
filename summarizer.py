# summarizer.py
def summarize_papers(papers):
    summaries = []
    for p in papers:
        if p["abstract"]:
            summaries.append(
                f"{p['year']}: {p['abstract'][:200]}..."
            )
    return summaries
