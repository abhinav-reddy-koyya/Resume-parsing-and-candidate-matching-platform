import os
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.parser import read_file
from utils.extractor import extract_all
from utils.job_matcher import match_resume_to_job
from utils.db import init_db, insert_resume, fetch_resumes, clear_db

# ------ Page setup ------
st.set_page_config(page_title="Resume Parsing Platform", layout="wide")
st.title("📄 Resume Parsing & Candidate Matching Platform")

# ------ Init DB ------
init_db()

# ------ Sidebar ------
st.sidebar.header("Controls")
with st.sidebar.expander("Database"):
    if st.button("Clear all parsed records ⚠️"):
        clear_db()
        st.success("Database cleared.")

st.sidebar.markdown("---")
st.sidebar.write("Tips:")
st.sidebar.caption("• Upload PDF/DOCX resumes on the first tab.\n"
                   "• Paste a Job Description to compute match %.\n"
                   "• Use the Dashboard tab for filtering & CSV export.\n"
                   "• Analytics tab shows top skills & match distribution.")

# ------ Tabs ------
tab1, tab2, tab3 = st.tabs(["📥 Upload & Parse", "📊 Candidate Dashboard", "📈 Analytics"])

# ------ Tab 1: Upload & Parse ------
with tab1:
    st.subheader("Upload Resumes")
    jd = st.text_area("Paste Job Description (optional, used for predicted score)",
                      height=140,
                      placeholder="Responsibilities, requirements, skills...")

    files = st.file_uploader("Upload PDF/DOCX resumes", type=["pdf", "docx"], accept_multiple_files=True)
    if files:
        os.makedirs("data/resumes", exist_ok=True)
        rows = []
        for f in files:
            save_path = os.path.join("data/resumes", f.name)
            with open(save_path, "wb") as out:
                out.write(f.getbuffer())

            text = read_file(save_path)
            if not text.strip():
                st.warning(f"Could not extract text from {f.name}. Skipping.")
                continue

            info = extract_all(text)
            predicted_score = match_resume_to_job(text, jd, info)

            row = {
                "filename": f.name,
                "name": info.get("name"),
                "email": info.get("email"),
                "phone": info.get("phone"),
                "skills": ", ".join(info.get("skills", [])),
                "education": json.dumps(info.get("education", {}), ensure_ascii=False),
                "experience": json.dumps(info.get("experience", {}), ensure_ascii=False),
                "predicted_score": predicted_score if predicted_score is not None else 0,
            }
            insert_resume(row)
            rows.append(row)

        if rows:
            df = pd.DataFrame(rows)
            st.success(f"Parsed {len(df)} resumes.")
            # Always show predicted_score
            st.dataframe(
                df[["filename", "name", "email", "phone", "skills", "predicted_score"]],
                use_container_width=True
            )
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download parsed CSV", csv, "parsed_resumes.csv", "text/csv")

# ------ Tab 2: Candidate Dashboard ------
with tab2:
    st.subheader("Parsed Candidates")
    df = fetch_resumes()

    if df.empty:
        st.info("No parsed candidates yet. Upload resumes first.")
    else:
        # Quick filters
        col1, col2, col3 = st.columns(3)
        with col1:
            q = st.text_input("Search keyword in skills/name/email", "")
        with col2:
            min_score = st.number_input("Min Predicted Score %", 0, 100, 0, step=1)
        with col3:
            has_email = st.selectbox("Require Email?", ["Either", "Yes", "No"])

        filtered = df.copy()
        if q:
            qlow = q.lower()
            filtered = filtered[
                filtered["skills"].fillna("").str.lower().str.contains(qlow)
                | filtered["name"].fillna("").str.lower().str.contains(qlow)
                | filtered["email"].fillna("").str.lower().str.contains(qlow)
            ]

        if "predicted_score" in filtered.columns:
            filtered = filtered[filtered["predicted_score"].fillna(0) >= min_score]

        if has_email == "Yes":
            filtered = filtered[filtered["email"].fillna("") != ""]
        elif has_email == "No":
            filtered = filtered[filtered["email"].fillna("") == ""]

        st.write(f"Showing {len(filtered)} of {len(df)} candidates")
        st.dataframe(
            filtered[["id", "filename", "name", "email", "phone", "skills", "predicted_score"]],
            use_container_width=True
        )

        dl_csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download filtered CSV", dl_csv, "candidates_filtered.csv", "text/csv")

# ------ Tab 3: Analytics ------
with tab3:
    st.subheader("Skills & Match Analytics")
    df = fetch_resumes()
    if df.empty:
        st.info("No analytics yet — parse some resumes first.")
    else:
        # Top skills
        all_skills = []
        for s in df["skills"].fillna(""):
            all_skills.extend([x.strip() for x in s.split(",") if x.strip()])
        if all_skills:
            top = pd.Series(all_skills).value_counts().head(12)
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(x=top.values, y=top.index, palette="viridis", ax=ax)
            ax.set_title("Top Skills Across Candidates")
            ax.set_xlabel("Count")
            ax.set_ylabel("Skill")
            st.pyplot(fig)
        else:
            st.info("No skills extracted yet.")

        # Predicted score distribution
        if "predicted_score" in df.columns and df["predicted_score"].notna().any():
            fig2, ax2 = plt.subplots(figsize=(7, 4))
            sns.histplot(df["predicted_score"].dropna(), bins=12, kde=True, color="#4c78a8", ax=ax2)
            ax2.set_title("Predicted Score Distribution")
            ax2.set_xlabel("Predicted Score %")
            st.pyplot(fig2)
        else:
            st.info("No predicted scores yet (add a job description when uploading).")
