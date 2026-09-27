import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv()


def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY is missing in the .env file."
        )

    return Anthropic(api_key=api_key)


def analyze_resume_with_claude(resume_text, job_description):
    """Analyze resume using Claude."""

    client = get_client()

    prompt = f"""
You are an expert resume and ATS analyzer.

Analyze the following resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON.

Use this format:

{{
    "summary": "short professional assessment",
    "strengths": [
        "strength 1",
        "strength 2",
        "strength 3"
    ],
    "weaknesses": [
        "weakness 1",
        "weakness 2"
    ],
    "recommendations": [
        "recommendation 1",
        "recommendation 2",
        "recommendation 3"
    ],
    "missing_keywords": [
        "keyword 1"
    ],
    "improved_summary": "improved professional summary"
}}

IMPORTANT:
- Do not invent experience.
- Do not invent companies.
- Do not invent certifications.
- Do not invent achievements.
- Base your analysis only on the supplied resume.
"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_text = response.content[0].text

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        return {
            "summary": response_text,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "missing_keywords": [],
            "improved_summary": "",
        }