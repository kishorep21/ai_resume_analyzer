from .ats_scoring import (
    get_matched_keywords,
    get_missing_keywords,
)


def analyze_keywords(resume_text, job_description):
    matched = get_matched_keywords(
        resume_text,
        job_description
    )

    missing = get_missing_keywords(
        resume_text,
        job_description
    )

    return {
        "matched": matched,
        "missing": missing,
    }