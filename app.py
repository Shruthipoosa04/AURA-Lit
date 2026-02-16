import streamlit as st
from paper_fetcher import fetch_papers
from timeline_builder import build_timeline
from summarizer import summarize_paper, extract_trends
import os
import openai

# -------------------- PAGE CONFIG -------------------- #
st.set_page_config(
    page_title="AURA-Lit AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM CSS (DARK THEME + CARD STYLES) -------------------- #
st.markdown("""
<style>
body, .stApp {
    background-color: #111111;
    color: #f5f5f5;
}
h1, h2, h3, h4 {
    color: #ffffff;
}
.stButton>button {
    background-color: #ffffff;
    color: #111111;
    font-weight: bold;
    border-radius: 8px;
}
.paper-card:hover {
    border-color: #888 !important;
    background-color: #1f1f1f !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR -------------------- #
st.sidebar.markdown("<h2 style='text-align:center;'>📚 AURA-Lit AI</h2>", unsafe_allow_html=True)

with st.sidebar.expander("ℹ️ About AURA-Lit", expanded=True):
    st.markdown("""
    **AURA-Lit** is an AI-agent-based research assistant that:
    - Retrieves academic papers from multiple sources  
    - Enforces a 10-year research timeline  
    - Builds year-wise research evolution  
    - Prepares data for LLM-based analysis  
    """)

with st.sidebar.expander("🧩 Development Phases", expanded=True):
    st.markdown("""
    **Phase 1:** Paper Retrieval & Timeline Construction  
    **Phase 2:** LLM-based Summarization  
    **Phase 3:** Trend & Insight Generation  
    """)

# -------------------- AI AGENT -------------------- #
class AURALitAgent:
    def __init__(self):
        self.thoughts = []

    def think(self, step):
        self.thoughts.append(step)

    def run(self, query):
        self.think("Understanding user research intent")
        self.think("Fetching papers from multiple academic sources")

        papers = fetch_papers(query, limit=15, years_back=10)

        if papers:
            self.think(f"Retrieved {len(papers)} papers across last 10 years")
        else:
            self.think("All academic sources unavailable or returned no results")

        self.think("Constructing year-wise research timeline")
        timeline = build_timeline(papers)

        return {
            "papers": papers,
            "timeline": timeline,
            "thoughts": self.thoughts
        }

# -------------------- HEADER -------------------- #
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
        placeholder="e.g., DeepFake Image Detection"
    )
    submitted = st.form_submit_button("🔍 Analyze")

# -------------------- EXECUTION -------------------- #
if submitted:
    if not research_title.strip():
        st.warning("⚠️ Please enter a valid research topic.")
    else:
        agent = AURALitAgent()
        with st.spinner("Analyzing academic literature..."):
            result = agent.run(research_title)

        # Initialize session state for summaries
        if "summaries" not in st.session_state:
            st.session_state.summaries = {}

        # -------------------- STATUS -------------------- #
        if result["papers"]:
            st.success(f"✅ {len(result['papers'])} papers retrieved across a 10-year timeline")
        else:
            st.warning("⚠️ Primary sources unavailable. Please try again later.")

        # -------------------- AGENT REASONING -------------------- #
        with st.expander("🤖 AURA-Agent Reasoning"):
            for t in result["thoughts"]:
                st.write("•", t)

        # -------------------- TIMELINE -------------------- #
        st.markdown("### 🕒 Research Evolution Timeline")
        if not result["timeline"]:
            st.info("Timeline will appear once papers are available.")
        else:
            for year, items in result["timeline"].items():
                with st.expander(f"🔹 {year} — {len(items)} paper(s)", expanded=False):
                    for p in items:
                        paper_id = p['title']  # unique key per paper

                        st.markdown(f"""
                        <div class='paper-card' style='background:#1b1b1b;padding:12px;border-radius:12px;
                                    margin-bottom:8px;border:1px solid #444;'>
                            <h4>{p['title']}</h4>
                            <p style='color:#bbbbbb;font-size:14px;'>
                            <i>{p['authors']}</i> | {p['source']}
                            </p>
                            <a href="{p['link']}" target="_blank">🔗 Read Paper</a>
                        </div>
                        """, unsafe_allow_html=True)

                        # --- Form per paper for summarize button ---
                        with st.form(key=f"summarize_form_{paper_id}"):
                            summarize_clicked = st.form_submit_button("🤖 Summarize")
                            if summarize_clicked:
                                with st.spinner("Generating summary..."):
                                    summary = summarize_paper(p['title'], p.get('abstract', ''))
                                    st.session_state.summaries[paper_id] = summary

                        # Display summary if it exists in session state
                        if paper_id in st.session_state.summaries:
                            st.markdown(f"**Summary:** {st.session_state.summaries[paper_id]}")
