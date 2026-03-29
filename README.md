# 🤖 SummarAI

SummarAI is an AI-powered web application that intelligently summarizes text and documents using a clean and modern user interface.

---

## 🚀 Features

- ✨ Smart text summarization
- 📄 Supports file uploads:
  - PDF
  - DOCX
  - CSV
  - TXT
- ⏳ Loading animation for better user experience
- ⬇ Download summarized output
- 🎨 Beautiful UI with gradient + background design
- 🔌 API endpoint for integration

---

## 🛠 Tech Stack

- Python
- Flask
- HTML, CSS, JavaScript
- Google Cloud Run (Deployment)

---

## 📂 Project Structure

SummarAI/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── agent/
└── venv/


---

## ▶️ How to Run Locally

```bash
venv\Scripts\activate
pip install -r requirements.txt
python app.py

Then open:

http://127.0.0.1:8080
☁️ Deployment

Deployed using Google Cloud Run:

gcloud run deploy summarai --source . --region asia-south1 --allow-unauthenticated
🎯 Use Case

SummarAI helps users quickly understand long content such as:

Academic notes
Resumes
Articles
Reports
