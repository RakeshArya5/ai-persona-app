import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PERSONAS = """
1. The Aspiring AI Engineer
2. The Non-Tech Explorer
3. The Tech Shifter
4. The Domain Climber
5. The AI Side-Hustler
6. The Academic Seeker
"""

def build_prompt(resume_text):
    return f"""
You are an AI career consultant. Based on the following resume:

1. Identify the best-fit persona from the following 6 types:
- The Aspiring AI Engineer
- The Non-Tech Explorer
- The Tech Shifter
- The Domain Climber
- The AI Side-Hustler
- The Academic Seeker

2. Output in this exact format:

<strong class='persona-heading'>The Tech Shifter</strong>

<strong>Summary of Background</strong>  
<paragraph>

<strong>Key Strengths</strong>  
<paragraph>

<strong>Realistic AI Opportunities They Can Aim For</strong>  
<paragraph>

<strong>What They Should Focus on Next</strong>  
<paragraph>

<strong>Final Note</strong>  
<paragraph>

Only output clean HTML-ready content — no numbers, no markdown, no bullet points. Just the persona name first, then the sections.

Resume:
\"\"\"
{resume_text}
\"\"\"
"""



def get_persona_profile(resume_text):
    prompt = build_prompt(resume_text)

    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful and realistic AI career consultant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content
