from openai import OpenAI
import streamlit as st
import time
from openai import RateLimitError

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def safe_chat_completion(messages, model="gpt-4o-mini", temperature=0.3):
    """
    Safe wrapper to prevent app crash during rate limit.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content

    except RateLimitError:
        return "⚠️ API rate limit reached. Please try again in a minute."

    except Exception as e:
        return f"⚠️ Error generating response."


# -------------------- SUMMARIZE -------------------- #
def summarize_paper(title, abstract):

    prompt = f"""
    Summarize this research paper:

    Title: {title}
    Abstract: {abstract}

    Include objective, method, findings, contribution.
    """

    messages = [
        {"role": "system", "content": "You are an academic research assistant."},
        {"role": "user", "content": prompt}
    ]

    return safe_chat_completion(messages)


# -------------------- TREND EXTRACTION -------------------- #
def extract_trends(papers):

    abstracts = "\n\n".join(
        [p.get("abstract", "") for p in papers if p.get("abstract")]
    )

    if not abstracts:
        return "Not enough abstracts available."

    prompt = f"""
    Analyze these abstracts and identify:
    - Dominant themes
    - Emerging trends
    - Common methodologies
    - Future directions

    {abstracts[:3000]}
    """

    messages = [
        {"role": "system", "content": "You are a research trend analyst."},
        {"role": "user", "content": prompt}
    ]

    return safe_chat_completion(messages, temperature=0.2)
