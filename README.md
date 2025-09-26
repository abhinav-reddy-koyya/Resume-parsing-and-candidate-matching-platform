📄 Resume Parsing & Candidate Matching Platform

📘 Summary

The Resume Parsing & Candidate Matching Platform is a Streamlit-powered recruitment assistant designed to simplify resume screening.
Recruiters can upload multiple resumes (PDF/DOCX), extract structured details (name, email, phone, skills, education, experience), and automatically compute a Predicted Match Score (%) against a job description.

The system provides:

A Candidate Dashboard to search and filter applicants

Analytics & Visualizations to see skills distribution and score histograms

SQLite database integration for persistence

CSV export for parsed and filtered candidate data

✨ Key Features
📥 Upload Resumes

Upload multiple resumes in PDF/DOCX format

Automatic text extraction and parsing of candidate details:

Name, email, phone

Skills, education, experience

📝 Job Description Matching

Paste a Job Description → system computes a Predicted Match Score (%) for each resume

Scores are saved in DB and exported in CSV

Score Colors:

🟢 Green ≥ 80 → Strong fit

🟠 Orange 50–79 → Medium fit

🔴 Red < 50 → Weak fit

📊 Candidate Dashboard

Search candidates by skills / name / email

Filter by minimum score or email availability

Export filtered candidate list as CSV

📈 Analytics Dashboard

Bar chart of top skills across all candidates

Histogram of Predicted Match Score distribution

💾 Database Integration

Uses SQLite (resume_db.sqlite3) for persistence

Resumes stay saved between runs

Option to reset/clear database

🛠 Tech Stack

Frontend/UI: Streamlit

Backend: Python 3 + SQLite

NLP: SpaCy (NER), Regex (email/phone)

Visualization: Matplotlib, Seaborn

Data Handling: Pandas

📂 Folder Structure
resume-parser/
│── app.py                 # Main Streamlit app
│── requirements.txt       # Dependencies
│── README.md              # Documentation
│
├── data/
│   ├── resumes/           # Uploaded resumes
│   └── parsed/            # Parsed CSVs
│   └── resume_db.sqlite3  # SQLite database
│
├── models/
│   └── skills.pkl         # Predefined skill set (for extraction)
│
├── utils/
│   ├── parser.py          # PDF/DOCX text reader
│   ├── extractor.py       # Extractor functions (skills, contact info, etc.)
│   ├── job_matcher.py     # JD vs Resume scoring logic
│   └── db.py              # SQLite database helpers

⚙️ Setup & Installation
1. Clone the repository
git clone https://github.com/your-username/resume-parser.git
cd resume-parser

2. Create a virtual environment
python -m venv venv


Activate it:

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

4. Download SpaCy model
python -m spacy download en_core_web_sm

5. Run the application
streamlit run app.py


Then open 👉 http://localhost:8501

🚀 Usage Guide
📥 Upload & Parse Tab

Upload resumes (PDF/DOCX)

(Optional) Paste a Job Description to compute match scores

Parsed resumes appear in a table with Predicted Score %

Export as CSV

📊 Candidate Dashboard Tab

Search candidates by skills, name, or email

Apply filters:

Minimum Predicted Score

Email required or not

Export filtered results as CSV

📈 Analytics Tab

View Top Skills Across Candidates (bar chart)

Visualize Predicted Score Distribution (histogram)

📊 Example Predicted Scores

90% (🟢 Green) → Excellent fit

65% (🟠 Orange) → Decent fit, may need training

40% (🔴 Red) → Weak fit

🔮 Future Improvements

Use TF-IDF / BERT embeddings for semantic JD–resume matching

Add experience duration extraction (years, roles, seniority)

Integration with external ATS systems

Deploy via Streamlit Cloud / AWS / Docker

✍️ Author: Built with ❤️ by Your Name

✅ This README now matches your final code — with predicted_score integrated everywhere.
