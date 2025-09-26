import re
from typing import Dict, List, Optional

import spacy

# Load small English model (run once in your env: python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None  # app will warn if not installed

# Extend/curate this as needed
SKILLS_DB = {
    "Programming": ["Python", "Java", "C++", "C#", "Go", "JavaScript", "TypeScript", "R", "SQL"],
    "Data/ML": ["Pandas", "NumPy", "scikit-learn", "TensorFlow", "PyTorch", "Keras", "XGBoost",
                "LightGBM", "Spark", "Hadoop", "Airflow", "ETL", "Tableau", "Power BI"],
    "Cloud/DevOps": ["AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform", "Jenkins", "Git"],
    "Web/Backend": ["Django", "Flask", "FastAPI", "Spring", "Node.js", "React", "Next.js"],
}

# Regexes
EMAIL_RE = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
PHONE_RE = re.compile(
    r"(?:(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4})"
)
# very permissive date span capture (e.g., Jan 2020 - Mar 2023)
DATE_SPAN_RE = re.compile(
    r"(?i)\b("
    r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\.?\s*\d{2,4}"
    r"|(?:\d{4})"
    r")\s*[-–to]{1,3}\s*("
    r"(?:present|current|\d{4}|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\.?\s*\d{2,4})"
    r")\b"
)

DEGREE_RE = re.compile(
    r"(?i)\b(B\.?Sc\.?|BSc|B\.?Eng\.?|BE|B\.?Tech|M\.?Sc\.?|MSc|M\.?Eng\.?|ME|M\.?Tech|MBA|Ph\.?D|B\.?A|M\.?A|B\.?Com|M\.?Com)\b"
)
UNIVERSITY_RE = re.compile(r"(?i)\b(university|institute|college|polytechnic)\b.*")


def extract_email(text: str) -> Optional[str]:
    m = EMAIL_RE.search(text)
    return m.group(0) if m else None


def extract_phone(text: str) -> Optional[str]:
    # pick the first that is at least 10 chars (to avoid false positives)
    matches = [m.group(0) for m in PHONE_RE.finditer(text)]
    matches = [m for m in matches if len(re.sub(r"\D", "", m)) >= 10]
    return matches[0] if matches else None


def extract_name(text: str) -> Optional[str]:
    if not nlp:
        return None
    doc = nlp(text[:2000])  # speed: first chunk often contains name header
    for ent in doc.ents:
        if ent.label_ == "PERSON" and 2 <= len(ent.text.split()) <= 4:
            return ent.text.strip()
    return None


def extract_skills(text: str) -> List[str]:
    found = set()
    low = text.lower()
    for group, skills in SKILLS_DB.items():
        for s in skills:
            if s.lower() in low:
                found.add(s)
    # Also pick simple patterns like 'machine learning', 'data science'
    keywords = ["machine learning", "deep learning", "data science", "nlp", "mlops"]
    for k in keywords:
        if k in low:
            found.add(k.title())
    return sorted(found)


def extract_education(text: str) -> Dict[str, List[str]]:
    degrees = [m.group(0) for m in DEGREE_RE.finditer(text)]
    institutions = []
    for line in text.splitlines():
        if UNIVERSITY_RE.search(line):
            institutions.append(line.strip())
    return {"degrees": degrees, "institutions": institutions[:6]}


def extract_experience(text: str) -> Dict[str, List[str]]:
    """
    Returns a minimal experience dict:
      - companies: ORG entities (spaCy)
      - date_spans: 'Jan 2020 - Mar 2023', '2019 - Present', etc.
    """
    companies = []
    if nlp:
        doc = nlp(text)
        companies = [e.text for e in doc.ents if e.label_ == "ORG"]

    date_spans = [m.group(0) for m in DATE_SPAN_RE.finditer(text)]
    return {"companies": companies[:12], "date_spans": date_spans[:12]}


def extract_all(text: str) -> Dict:
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
    }
