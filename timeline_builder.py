from collections import defaultdict
from datetime import datetime

def build_timeline(papers, years_back=10):
    """
    Builds a timeline of papers grouped by year.

    Args:
        papers (list of dict): Each dict should have keys 'title', 'authors', 'year', 'source', 'link'.
        years_back (int): Number of years to include in the timeline (default 10).

    Returns:
        dict: Timeline dictionary with year as key and list of papers as value, sorted by year descending.
              Only includes years that have papers.
    """
    timeline = defaultdict(list)
    current_year = datetime.now().year
    start_year = current_year - years_back

    for paper in papers:
        year = paper.get("year")
        if year and start_year <= year <= current_year:
            timeline[year].append({
                "title": paper.get("title"),
                "authors": paper.get("authors"),
                "source": paper.get("source"),
                "link": paper.get("link")
            })

    # Remove years with no papers
    timeline = {year: items for year, items in timeline.items() if items}

    # Return timeline sorted by year descending
    return dict(sorted(timeline.items(), reverse=True))
