import re


COMMON_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "sql",
    "html",
    "css",
    "react",
    "node.js",
    "node",
    "express",
    "mongodb",
    "mysql",
    "postgresql",
    "aws",
    "azure",
    "google cloud",
    "gcp",
    "docker",
    "kubernetes",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "genai",
    "generative ai",
    "tensorflow",
    "pytorch",
    "power bi",
    "tableau",
}


def normalize_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_keywords(text):
    text = normalize_text(text)

    found = set()

    for skill in COMMON_SKILLS:
        if skill in text:
            found.add(skill)

    return found


def keyword_match_score(resume_text, job_description):
    if not job_description.strip():
        return 0

    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    if not job_keywords:
        return 0

    matched = resume_keywords.intersection(job_keywords)

    return round((len(matched) / len(job_keywords)) * 100)


def skills_score(resume_text, job_description):
    return keyword_match_score(resume_text, job_description)


def contact_score(resume_text):
    score = 0

    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"

    if re.search(email_pattern, resume_text):
        score += 50

    phone_pattern = r"\+?\d[\d\s\-]{8,}\d"

    if re.search(phone_pattern, resume_text):
        score += 50

    return score


def formatting_score(resume_text):
    score = 100

    if len(resume_text) < 300:
        score -= 30

    if len(resume_text.split()) < 100:
        score -= 20

    if "experience" not in resume_text.lower():
        score -= 15

    if "education" not in resume_text.lower():
        score -= 15

    if "skills" not in resume_text.lower():
        score -= 15

    return max(0, score)


def calculate_ats_score(resume_text, job_description=""):
    """
    Calculate an ATS-style resume score.

    Returns a dictionary containing score components.
    """

    keyword_score = keyword_match_score(
        resume_text,
        job_description
    )

    skill_score = skills_score(
        resume_text,
        job_description
    )

    contact = contact_score(resume_text)

    formatting = formatting_score(resume_text)

    if job_description.strip():
        overall = (
            keyword_score * 0.30
            + skill_score * 0.20
            + formatting * 0.15
            + contact * 0.10
            + 50 * 0.25
        )
    else:
        overall = (
            formatting * 0.40
            + contact * 0.20
            + 50 * 0.40
        )

    return {
        "overall_score": round(overall),
        "keyword_score": keyword_score,
        "skills_score": skill_score,
        "formatting_score": formatting,
        "contact_score": contact,
    }


def get_matched_keywords(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    return sorted(resume_keywords.intersection(job_keywords))


def get_missing_keywords(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    return sorted(job_keywords - resume_keywords)