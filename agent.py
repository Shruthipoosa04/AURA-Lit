# agent.py
from paper_fetcher import fetch_papers
from summarizer import summarize_papers
from timeline_builder import build_timeline

class AURALitAgent:
    def __init__(self):
        self.thoughts = []

    def log(self, message):
        self.thoughts.append(message)

    def run(self, query):
        self.log("Understanding research intent")
        
        self.log("Fetching relevant academic papers")
        papers = fetch_papers(query)

        self.log("Summarizing existing systems from abstracts")
        summaries = summarize_papers(papers)

        self.log("Building year-wise evolution timeline")
        timeline = build_timeline(papers)

        return {
            "papers": papers,
            "summaries": summaries,
            "timeline": timeline,
            "agent_thoughts": self.thoughts
        }
