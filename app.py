import streamlit as st
from paper_fetcher import fetch_papers
from timeline_builder import build_timeline
# from summarizer import summarize_paper, extract_trends
import os
import openai

# -------------------- PAGE CONFIG -------------------- #
st.set_page_config(
    page_title="AURA-Lit AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM CSS -------------------- #
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
.summary-card {
    background:#181818;
    padding:15px;
    border-radius:12px;
    margin-top:10px;
    border:1px solid #333;
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
        self.think("🔎 Understanding research intent")
        self.think("📚 Fetching papers from academic sources")

        papers = fetch_papers(query, limit=15, years_back=10)

        if papers:
            self.think(f"✅ Retrieved {len(papers)} papers from last 10 years")
        else:
            self.think("⚠️ No results returned from sources")

        self.think("🕒 Constructing year-wise research timeline")
        timeline = build_timeline(papers)

        #self.think("📊 Extracting research trends")
        #trends = extract_trends(papers)

        return {
            "papers": papers,
            "timeline": timeline,
            "thoughts": self.thoughts,
           # "trends": trends
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

        with st.spinner("🤖 AURA-Agent analyzing literature..."):
            result = agent.run(research_title)

        # Initialize session state
        if "summaries" not in st.session_state:
            st.session_state.summaries = {}

        # -------------------- STATUS -------------------- #
        if result["papers"]:
            st.success(f"✅ {len(result['papers'])} papers retrieved across a 10-year timeline")
        else:
            st.warning("⚠️ No papers found.")

        # -------------------- AGENT REASONING -------------------- #
        with st.expander("🤖 AURA-Agent Reasoning", expanded=False):
            for t in result["thoughts"]:
                st.write(t)

        # -------------------- TRENDS -------------------- #
        #st.markdown("### 📈 Research Trends & Insights")
        #if result["trends"]:
         #   st.info(result["trends"])
        #else:
         #   st.info("Trend insights will appear once sufficient papers are available.")

        # -------------------- TIMELINE -------------------- #
        st.markdown("### 🕒 Research Evolution Timeline")

        if not result["timeline"]:
            st.info("Timeline will appear once papers are available.")
        else:
            for year, items in result["timeline"].items():
                with st.expander(f"🔹 {year} — {len(items)} paper(s)", expanded=False):

                    for p in items:
                        paper_id = f"{year}_{p['title']}"

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

                        # -------- Summarize Button -------- #
                       # if st.button("🤖 Summarize", key=f"btn_{paper_id}"):

                        #    with st.spinner("Generating AI summary..."):
                         #       summary = summarize_paper(
                          #          p['title'],
                           #         p.get('abstract', '')
                            #    )
                             #   st.session_state.summaries[paper_id] = summary

                        # -------- Display Summary -------- #
                        if paper_id in st.session_state.summaries:
                            st.markdown(f"""
                            <div class='summary-card'>
                                <b>AI Summary:</b><br><br>
                                {st.session_state.summaries[paper_id]}
                            </div>
                            """, unsafe_allow_html=True)
