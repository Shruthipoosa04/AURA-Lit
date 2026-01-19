import streamlit as st
import requests
from collections import defaultdict
from datetime import datetime

# -------------------- PAGE CONFIG -------------------- #
st.set_page_config(
    page_title="AURA-Lit AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM CSS (DARK THEME) -------------------- #
st.markdown("""
<style>
body, .stApp {
    background-color: #111111;
    color: #f5f5f5;
}
h1, h2, h3 {
    color: #ffffff;
}
.stButton>button {
    background-color: #ffffff;
    color: #111111;
    font-weight: bold;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR -------------------- #
st.sidebar.markdown("<h2 style='text-align:center;'>📚 AURA-Lit AI</h2>", unsafe_allow_html=True)

with st.sidebar.expander("ℹ️ About AURA-Lit", expanded=True):
    st.markdown("""
    **AURA-Lit** is an AI-agent-based research assistant that:
    - Retrieves academic papers
    - Extracts existing systems
    - Builds year-wise research evolution
    """)

with st.sidebar.expander("🔍 Development Phases", expanded=True):
    st.markdown("""
    **Phase 1:** Paper Retrieval  
    **Phase 2:** System Extraction  
    **Phase 3:** Trend & Insight Generation  
    """)

# -------------------- AI TOOLS -------------------- #
def fetch_papers(query, limit=5):
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,abstract,url"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json().get("data", [])

        papers = []
        for p in data:
            papers.append({
                "title": p.get("title", "N/A"),
                "authors": ", ".join([a["name"] for a in p.get("authors", [])[:3]]),
                "year": p.get("year", "N/A"),
                "abstract": p.get("abstract", ""),
                "link": p.get("url", "#")
            })
        return papers
    except:
        return []

def summarize_papers(papers):
    summaries = []
    for p in papers:
        if p["abstract"]:
            summaries.append(f"{p['year']}: {p['abstract'][:180]}...")
    return summaries

def build_timeline(papers):
    timeline = defaultdict(list)
    for p in papers:
        timeline[p["year"]].append(p["title"])
    return dict(sorted(timeline.items(), reverse=True))

# -------------------- AI AGENT -------------------- #
class AURALitAgent:
    def __init__(self):
        self.thoughts = []

    def think(self, step):
        self.thoughts.append(step)

    def run(self, query):
        self.think("Understanding user research intent")
        self.think("Selecting paper retrieval tool")

        papers = fetch_papers(query)

        if papers:
            self.think("Papers retrieved successfully")
            self.think("Summarizing existing systems")
        else:
            self.think("API failed, switching to fallback knowledge")

        summaries = summarize_papers(papers)
        self.think("Building year-wise research evolution")

        timeline = build_timeline(papers)

        return {
            "papers": papers,
            "summaries": summaries,
            "timeline": timeline,
            "thoughts": self.thoughts
        }

# -------------------- MAIN HEADER -------------------- #
st.markdown("""
<div style='background:#1a1a1a;padding:30px;border-radius:15px;text-align:center;margin-bottom:20px;'>
<h1>📚 AURA-Lit – AI Research Agent</h1>
<p style='color:#cccccc;font-size:16px;'>
An AI-agent-driven system for automated literature understanding.
</p>
</div>
""", unsafe_allow_html=True)

# -------------------- INPUT FORM -------------------- #
with st.form("research_form"):
    research_title = st.text_input(
        "📝 Enter Research Topic",
        placeholder="e.g., AI-driven IoT Security Framework"
    )
    submitted = st.form_submit_button("🔍 Analyze")

# -------------------- AGENT EXECUTION -------------------- #
if submitted:
    if not research_title.strip():
        st.warning("⚠️ Please enter a research title.")
    else:
        agent = AURALitAgent()
        result = agent.run(research_title)

        st.success(f"Analyzing: {research_title}")

        # -------------------- AGENT REASONING -------------------- #
        with st.expander("🤖 AURA-Agent Reasoning"):
            for t in result["thoughts"]:
                st.write("•", t)

        col1, col2 = st.columns([2, 3])

        # -------------------- PAPERS -------------------- #
        with col1:
            st.markdown("### 📄 Relevant Papers")

            if not result["papers"]:
                st.info("No papers retrieved. API may be unavailable.")
            else:
                for p in result["papers"]:
                    st.markdown(f"""
                    <div style='background:#1b1b1b;padding:15px;border-radius:12px;margin-bottom:12px;border:1px solid #444;'>
                        <h4>{p['title']}</h4>
                        <p style='color:#bbbbbb;font-size:14px;'>
                        <i>{p['authors']}</i> | {p['year']}
                        </p>
                        <a href="{p['link']}" target="_blank">🔗 Read Paper</a>
                    </div>
                    """, unsafe_allow_html=True)

        # -------------------- TIMELINE -------------------- #
        with col2:
            st.markdown("### 🕒 Existing Systems Timeline")

            if not result["timeline"]:
                st.info("Timeline will appear once papers are available.")
            else:
                for year, titles in result["timeline"].items():
                    st.markdown(f"""
                    <div style='background:#1b1b1b;padding:12px;border-radius:12px;margin-bottom:10px;border:1px solid #444;'>
                        <b>{year}</b><br>
                        <span style='color:#bbbbbb;font-size:14px;'>
                        {", ".join(titles[:2])}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
