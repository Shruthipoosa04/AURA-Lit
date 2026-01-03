import streamlit as st
from datetime import datetime

# -------------------- PAGE CONFIG -------------------- #
st.set_page_config(
    page_title="AURA-Lit AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM CSS FOR DARK THEME -------------------- #
st.markdown(
    """
    <style>
    /* Background and text */
    body, .stApp, .css-18e3th9 {
        background-color: #111111;
        color: #f5f5f5;
    }
    /* Sidebar */
    .css-1d391kg {
        background-color: #1a1a1a;
        color: #f5f5f5;
        padding: 20px;
    }
    /* Headers */
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    /* Buttons */
    .stButton>button {
        background-color: #ffffff;
        color: #111111;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
    }
    /* Cards */
    .paper-card {
        background-color: #1e1e1e;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #333333;
    }
    a {
        color: #ffffff;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True
)

# -------------------- SIDEBAR -------------------- #
st.sidebar.markdown("<h2 style='color:white; text-align:center;'>📚 AURA-Lit AI</h2>", unsafe_allow_html=True)

# -------------------- Description -------------------- #
with st.sidebar.expander("ℹ️ About AURA-Lit", expanded=True):
    st.markdown("""
    <div style='padding:10px; background-color:#1a1a1a; border-radius:10px;'>
    <p style='color:#dcdcdc; font-size:14px; line-height:1.5'>
    <strong>AURA-Lit:</strong> Automated Understanding of Research Articles.  
    Enter a research title and get:
    <ul>
    <li>Relevant academic papers</li>
    <li>Year-wise evolution of existing systems</li>
    </ul>
    </p>
    </div>
    """, unsafe_allow_html=True)

# -------------------- Input Section -------------------- #
with st.sidebar.expander("📝 Submit Research Title", expanded=True):
    st.markdown("""
    <p style='color:#dcdcdc; font-size:14px; line-height:1.5'>
    Use the main page input form to enter your research topic.  
    You can also enter keywords to refine results.
    </p>
    """, unsafe_allow_html=True)
    keywords = st.text_input("🔑 Keywords (optional)", "")
    category_filter = st.selectbox(
        "📂 Filter by Category (optional)",
        ["All", "Machine Learning", "Cybersecurity", "IoT", "Data Science"]
    )

# -------------------- Phases Section -------------------- #
with st.sidebar.expander("🔍 Development Phases", expanded=True):
    st.markdown("""
    <div style='padding:10px; background-color:#1a1a1a; border-radius:10px;'>
    <p style='color:#dcdcdc; font-size:13px; line-height:1.5'>
    <b>Phase 1:</b> Paper retrieval & relevance filtering  
    <span title="Fetch top relevant papers using Semantic Scholar API.">ℹ️</span><br>
    <b>Phase 2:</b> Existing system extraction & timeline summary  
    <span title="Analyze papers and generate year-wise summaries.">ℹ️</span><br>
    <b>Phase 3:</b> Advanced summarization & trend analysis  
    <span title="Generate insights and trends from historical research.">ℹ️</span>
    </p>
    </div>
    """, unsafe_allow_html=True)

# -------------------- Tips Section -------------------- #
with st.sidebar.expander("💡 Tips & Recommendations", expanded=True):
    st.markdown("""
    <div style='padding:10px; background-color:#1a1a1a; border-radius:10px; border-left:3px solid #ffffff'>
    <p style='color:#dcdcdc; font-size:13px; line-height:1.5'>
    - Enter concise research titles for better results.<br>
    - Use relevant keywords separated by commas.<br>
    - Apply filters to narrow paper search.<br>
    - Hover over ℹ️ icons in Phases for more info.
    </p>
    </div>
    """, unsafe_allow_html=True)


# -------------------- MAIN PAGE -------------------- #
st.markdown("""
<div style='background-color:#1a1a1a; padding:30px; border-radius:15px; text-align:center; margin-bottom:20px;'>
    <h1 style='color:white; margin-bottom:10px;'>📚 AURA-Lit – Your Research Assistant</h1>
    <p style='color:#dcdcdc; font-size:18px; line-height:1.6; max-width:800px; margin:auto;'>
    AI-powered tool to help researchers quickly understand relevant papers, 
    summarize existing systems, and visualize the evolution of techniques over time.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------- INPUT FORM -------------------- #
with st.form(key="research_form"):
    st.markdown("<h3 style='color:white;'>📝 Enter Your Research Topic</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#dcdcdc; font-size:14px; line-height:1.5'>
    Type the research title or keywords below. Use commas to separate multiple keywords for more accurate results.
    </p>
    """, unsafe_allow_html=True)
    
    research_title = st.text_input("", placeholder="e.g., 'AI-driven IoT Security Framework'")
    
    submitted = st.form_submit_button("🔍 Analyze", help="Click to fetch relevant papers and summarize existing systems")

# -------------------- FEEDBACK / RESULTS PLACEHOLDER -------------------- #
if submitted:
    if not research_title.strip():
        st.warning("⚠️ Please enter a research title to analyze.")
    else:
        # Success alert with styled box
        st.markdown(f"""
        <div style='background-color:#111111; border-left:5px solid #ffffff; padding:15px; border-radius:8px; margin-bottom:15px;'>
            <b>Analyzing Research Topic:</b> <span style='color:#ffffff'>{research_title}</span><br>
            <span style='color:#dcdcdc;'>Fetching relevant papers and generating summaries... (Phase 1 in progress)</span>
        </div>
        """, unsafe_allow_html=True)
      # -------------------- TWO COLUMNS LAYOUT -------------------- #
col1, col2 = st.columns([2, 3])

# ---------- LEFT COLUMN: Paper Cards ---------- #
with col1:
    st.markdown("<h3 style='color:white;'>📄 Relevant Papers</h3>", unsafe_allow_html=True)
    st.info("Paper metadata will appear here once retrieval is implemented.")

    example_papers = [
        {"title": "AI-driven IoT Security", "authors": "Author A et al.", "year": "2023", "link": "#"},
        {"title": "ML for Cyber Defense", "authors": "Author B et al.", "year": "2022", "link": "#"},
        {"title": "Deep Learning Threat Detection", "authors": "Author C et al.", "year": "2021", "link": "#"},
    ]

    for paper in example_papers:
        st.markdown(f"""
        <div style='background-color:#1b1b1b; padding:15px; border-radius:12px; margin-bottom:15px; border:1px solid #444; transition: transform 0.2s;'>
            <h4 style='color:#ffffff; margin-bottom:5px;'>{paper['title']}</h4>
            <p style='color:#bbbbbb; margin:0; font-size:14px;'><i>{paper['authors']}</i> | {paper['year']}</p>
            <a href='{paper['link']}' target='_blank' style='color:#1ecbe1; text-decoration:none; font-size:14px;'>🔗 Read Paper</a>
        </div>
        """, unsafe_allow_html=True)

# ---------- RIGHT COLUMN: Timeline ---------- #
with col2:
    st.markdown("<h3 style='color:white;'>🕒 Existing Systems Timeline</h3>", unsafe_allow_html=True)
    st.info("Year-wise summaries of techniques will appear here.")

    timeline_events = [
        {"year_range": "2015-2018", "desc": "Rule-based methods dominate."},
        {"year_range": "2019-2021", "desc": "Machine learning approaches improve detection."},
        {"year_range": "2022-Present", "desc": "Deep learning & hybrid models reduce false positives."}
    ]

    # Create timeline with visual markers
    for event in timeline_events:
        st.markdown(f"""
        <div style='display:flex; align-items:flex-start; margin-bottom:15px;'>
            <div style='width:10px; height:10px; background-color:#ffffff; border-radius:50%; margin-top:6px; margin-right:10px;'></div>
            <div style='background-color:#1b1b1b; padding:12px 15px; border-radius:12px; border:1px solid #444; flex:1;'>
                <b style='color:#ffffff;'>{event['year_range']}</b><br>
                <span style='color:#bbbbbb; font-size:14px;'>{event['desc']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
