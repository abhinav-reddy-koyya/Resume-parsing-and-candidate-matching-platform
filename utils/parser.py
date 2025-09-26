import os
from typing import Optional
from io import BytesIO

import docx
from pdfminer.high_level import extract_text


def read_pdf(path: str) -> str:
    try:
        return extract_text(path) or ""
    except Exception as e:
        return f""  # keep silent failure; upstream will handle empty text


def read_docx(path: str) -> str:
    try:
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception:
        return ""


def read_file(path: str) -> str:
    """
    Read a resume file (.pdf or .docx) and return plain text.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return read_pdf(path)
    elif ext == ".docx":
        return read_docx(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
