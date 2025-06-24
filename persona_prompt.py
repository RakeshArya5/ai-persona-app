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
You are an AI career consultant helping learners identify their AI path based on their resume.

Here are the 6 possible personas:
{PERSONAS}

Based on the following resume, do the following:
1. Identify which one of the 6 personas best fits the individual.
2. Generate a structured profile report with these sections:
   - Summary of background
   - Key strengths
   - Realistic AI opportunities they can aim for
   - What they should focus on next
   - Final note to motivate and direct them

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
