import streamlit as st
from paper_fetcher import fetch_papers
from timeline_builder import build_timeline
from summarizer import predict_contribution

# -------------------- PAGE CONFIG -------------------- #
st.set_page_config(
    page_title="AURA-Lit AI",
    page_icon="📑",
    layout="wide"
)

# -------------------- MODERN SAAS CSS -------------------- #
 
st.markdown("""
<style>

/* =========================
   GLOBAL BACKGROUND
========================= */
.stApp {
    background: linear-gradient(135deg,#0f1117,#0b0c10);
    color: white;
    font-family: 'Inter', sans-serif;
    animation: fadeIn 0.6s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #2d3748;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #4fd1c5;
}

/* =========================
   SIDEBAR
========================= */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364)
    border-right: 1px solid #2d3748;
    padding-top: 20px;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
     
}

/* Section headers */
.sidebar-section-title {
    font-size: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #9ca3af;
    margin-top: 24px;
    margin-bottom: 8px;
}

/* Card blocks inside sidebar */
.sidebar-card {
    background: rgba(255, 255, 255, 0.04);
    padding: 14px 16px;
    border-radius: 12px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.05);
    transition: all 0.25s ease;
}

.sidebar-card:hover {
    border: 1px solid #4fd1c5;
    box-shadow: 0 0 15px rgba(79,209,197,0.25);
}

/* Status badge */
.status-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 14px;
    background: linear-gradient(135deg,#4fd1c5,#63b3ed);
    color: #22c55e;
    font-weight: 500;
}

/* =========================
   HERO HEADER
========================= */
.header-box {
    padding: 40px 0px;
    text-align: center;
    margin-bottom: 40px;
}

.header-box h1 {
    font-size: 42px;
    letter-spacing: 1px;
}

.header-box p {
    opacity: 0.75;
}

/* =========================
   INPUT FIELD
========================= */
.stTextInput > div > div > input {
    background: #161a22;
    border: 1px solid #2d3748;
    border-radius: 10px;
    color: white;
    padding: 12px;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border: 1px solid #4fd1c5;
    box-shadow: 0 0 12px rgba(79,209,197,0.5);
    outline: none;
}

/* =========================
   PAPER CARD
========================= */
.paper-card {
    background: #161a22;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 16px;
    border: 1px solid #2d3748;
    transition: all 0.3s ease;
}

.paper-card:hover {
    transform: translateY(-4px);
    border: 1px solid #4fd1c5;
    box-shadow: 0 15px 35px rgba(0,0,0,0.45);
}

/* =========================
   SUMMARY CARD
========================= */
.summary-card {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    padding: 24px;
    border-radius: 16px;
    margin-top: 15px;
    border: 1px solid #4fd1c5;
    box-shadow: 0px 0px 20px rgba(79,209,197,0.25);
    color: #e2e8f0;
    line-height: 1.7;
    max-width: 750px;
    transition: all 0.3s ease;
}

.summary-card:hover {
    box-shadow: 0px 0px 30px rgba(79,209,197,0.4);
    transform: scale(1.01);
}

.summary-card h3 {
    margin-top: 0;
    color: linear-gradient(135deg,#4fd1c5,#63b3ed);
}

/* =========================
   BUTTONS
========================= */
.stButton > button {
    background: linear-gradient(135deg,#4fd1c5,#63b3ed);
    color: black;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    padding: 0.6rem 1.4rem;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(79,209,197,0.4);
}

/* =========================
   METRICS
========================= */
[data-testid="metric-container"] {
    background: #161a22;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #2d3748;
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    border: 1px solid #4fd1c5;
    box-shadow: 0 0 12px rgba(79,209,197,0.3);
}
</style>
""", unsafe_allow_html=True)

# -------------------- HERO -------------------- #
st.markdown("""
<div class="header-box">
    <h1>📑 AURA-Lit </h1>
    <h4>Advanced Unified Research Analytics for Literature Intelligence</h4>
    <p>
    Discover, analyze, and forecast academic research with structured insights,
    timeline evolution, and contribution prediction.
    </p>
</div>
""", unsafe_allow_html=True)


st.sidebar.markdown("""
<h2 style="margin-bottom:5px;">AURA-Lit</h2>
<span class="status-badge">● AI Engine Online</span>
<p style="font-size:13px; opacity:0.7; margin-top:10px;">
Academic Research Intelligence Platform
</p>

<div class="sidebar-section-title">Platform Overview</div>

<div class="sidebar-card">
Transform raw academic literature into structured, actionable intelligence.
</div>

<div class="sidebar-section-title">Core Capabilities</div>

<div class="sidebar-card">
 Retrieve up to <b>100</b> peer-reviewed papers<br>
 Coverage: <b>2000 → Present</b><br>
 Research evolution analytics<br>
 AI-driven contribution forecasting<br>
 Innovation & impact scoring
</div>

<div class="sidebar-section-title">System Metrics</div>

<div class="sidebar-card">
 Real-time API aggregation<br>
 Multi-domain inference engine<br>
 Confidence-based evaluation
</div>

<hr style="opacity:0.1; margin-top:20px;">

<p style="font-size:12px; opacity:0.5;">
Version 2.1 • Research Intelligence Suite
</p>
""", unsafe_allow_html=True)


# -------------------- SESSION STATE -------------------- #
if "summaries" not in st.session_state:
    st.session_state.summaries = {}

if "result" not in st.session_state:
    st.session_state.result = None

# -------------------- AGENT -------------------- #
class AURALitAgent:

    def __init__(self):
        self.thoughts = []
        self.metadata = {}

    def think(self, message):
        self.thoughts.append(message)

    def run(self, query):

        self.thoughts = []
        cleaned_query = query.strip()

        self.think("Analyzing research query intent")
        self.think("Retrieving academic publications (2000 → Present)")

        papers = fetch_papers(
            query=cleaned_query,
            limit=100,
            start_year=2000
        )

        self.think(f"Retrieved {len(papers)} papers")

        self.think("Constructing chronological research timeline")
        timeline = build_timeline(papers)

        self.think("Timeline construction completed")

        return {
            "papers": papers,
            "timeline": timeline,
            "thoughts": self.thoughts
        }

# -------------------- SEARCH FORM -------------------- #
with st.form("search_form"):
    topic = st.text_input(
        "🔍 Enter Research Topic",
        placeholder="e.g., Cyber Deception Techniques"
    )
    submit = st.form_submit_button("Analyze")

# -------------------- EXECUTION -------------------- #
if submit:
    if not topic.strip():
        st.warning("Please enter a research topic")
        st.stop()

    agent = AURALitAgent()

    with st.spinner("Analyzing research landscape..."):
        st.session_state.result = agent.run(topic)

# -------------------- RESULTS -------------------- #
if st.session_state.result:

    result = st.session_state.result
    timeline = result["timeline"]

    with st.expander("🤖 Agent Reasoning"):
        for t in result["thoughts"]:
            st.write("•", t)

    st.markdown("## 🕒 Research Evolution Timeline")

    if not timeline:
        st.info("No timeline available")

    else:
        for year, items in timeline.items():

            with st.expander(f"📆 {year} — {len(items)} papers"):

                for idx, p in enumerate(items):

                    paper_id = f"{year}_{idx}"

                    # Paper Card
                    st.markdown(f"""
                    <div class="paper-card">
                        <h4>{p['title']}</h4>
                        <p style="color:#9ca3af; font-size:14px;">
                            {p['authors']} | {p['source']}
                        </p>
                        <a href="{p['link']}" target="_blank" style="color:#4fd1c5;">
                            📄 View Publication
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

                    # Predict Button
                    if st.button("Predict Contribution", key=f"btn_{paper_id}"):

                        if paper_id not in st.session_state.summaries:
                            with st.spinner("Analyzing Research Contribution..."):
                                insight = predict_contribution(p["title"])
                                st.session_state.summaries[paper_id] = insight

                    # Summary Display
                    if paper_id in st.session_state.summaries:

                        data = st.session_state.summaries[paper_id]

                        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                        st.markdown("### Research Summary")
                        st.write(data["paragraph"])

                        col1, col2 = st.columns(2)
                        col1.metric("Confidence Score", f"{data['confidence']}%")
                        col2.metric("Innovation Level", data["novelty"])

                        st.markdown("**Potential Impact**")
                        st.write(data["impact"])

                        st.markdown('</div>', unsafe_allow_html=True)