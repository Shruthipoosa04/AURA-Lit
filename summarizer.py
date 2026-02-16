from openai import OpenAI
import os

# Create client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------- SUMMARIZE -------------------- #
def summarize_paper(title, abstract):

    prompt = f"""
    Summarize the following research paper in 150-200 words.
    
    Title: {title}
    Abstract: {abstract}
    
    Provide:
    - Core objective
    - Methodology
    - Key findings
    - Contribution
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # lightweight + cheaper
        messages=[
            {"role": "system", "content": "You are an academic research assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# -------------------- TREND EXTRACTION -------------------- #
def extract_trends(papers):

    abstracts = "\n\n".join(
        [p.get("abstract", "") for p in papers if p.get("abstract")]
    )

    if not abstracts:
        return "Not enough data for trend analysis."

    prompt = f"""
    Analyze the following research abstracts and identify:
    - Dominant research themes
    - Emerging trends
    - Frequently used methodologies
    - Future research directions

    Abstracts:
    {abstracts[:4000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an academic research analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
