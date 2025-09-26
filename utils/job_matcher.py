import re

def clean_text(text):
    """Lowercase and remove non-alphanumeric characters."""
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())

def match_resume_to_job(resume_text: str, job_description: str, parsed_info: dict = None) -> float:
    """
    Match resume text against job description text.
    Uses keywords, skills, education, and experience for scoring.
    Returns a predicted score (0-100).
    """
    if not job_description.strip():
        return 0.0

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    resume_words = set(resume_text.split())
    job_words = set(job_description.split())

    if not job_words:
        return 0.0

    # --- Base overlap score ---
    overlap = resume_words.intersection(job_words)
    base_score = (len(overlap) / len(job_words)) * 60  # max 60%

    # --- Skills bonus ---
    skill_score = 0
    if parsed_info and "skills" in parsed_info:
        skills = [s.lower() for s in parsed_info.get("skills", [])]
        job_skills = [w for w in job_words if len(w) > 2]
        matches = sum(1 for s in skills if s in job_skills)
        if job_skills:
            skill_score = (matches / len(job_skills)) * 30  # max 30%

    # --- Education / Experience bonus ---
    edu_exp_bonus = 0
    if parsed_info:
        if parsed_info.get("education"):
            edu_exp_bonus += 5
        if parsed_info.get("experience"):
            edu_exp_bonus += 5

    final_score = min(100, base_score + skill_score + edu_exp_bonus)
    return round(final_score, 2)
