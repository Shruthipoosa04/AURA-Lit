# summarizer.py
import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]


def summarize_paper(title, abstract):
    """
    Summarize a single academic paper using GPT.
    """
    prompt = f"Summarize this academic paper concisely:\nTitle: {title}\nAbstract: {abstract}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def extract_trends(papers):
    """
    Extract trends and insights from a list of papers.
    """
    abstracts = "\n".join([p.get('abstract','') for p in papers])
    prompt = f"Analyze these academic papers and provide:\n- Top topics\n- Emerging trends\n- Common methodologies\n\nAbstracts:\n{abstracts}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
