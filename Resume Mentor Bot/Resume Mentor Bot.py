# Bot 1 - Resume Mentor Bot

# Install Libraries

!pip install -q streamlit pyngrok groq pypdf python-docx

# Streamlit App

streamlit_code = """
import streamlit as st
from groq import Groq
from pypdf import PdfReader
from docx import Document
import os
# --------------------
# Setup Groq client
# --------------------
# Directly read from environment variable
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
st.set_page_config(page_title="Resume Mentor Bot", layout="wide")
st.title("📄 Resume Mentor Bot")
st.write("Upload your resume (PDF/DOCX/TXT) for analysis.")
# --------------------
# Extract text from file
# --------------------
def extract_text(file):
    if file.type == "application/pdf":
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        doc = Document(file)
        return "\\n".join([p.text for p in doc.paragraphs])
    else:
        return file.read().decode("utf-8")
# --------------------
# Analyze resume using Groq LLM
# --------------------
def analyze_resume(text):
    prompt = f\"\"\"
You are Resume Mentor Bot.
Analyze this resume and provide:
1. Overall Resume Score (0–100)
2. Key Strengths
3. Weaknesses / Red Flags
4. ATS Compatibility
5. Suggestions to Improve Resume
6. Missing Skills
7. Job Roles Suitable
Resume Content:
{text}
\"\"\"
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1200
    )
    return response.choices[0].message.content
# --------------------
# Streamlit UI
# --------------------
uploaded_file = st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf", "docx", "txt"])
if uploaded_file:
    st.success("File uploaded successfully!")
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing your resume..."):
            text = extract_text(uploaded_file)
            result = analyze_resume(text)
        st.subheader("📌 Resume Analysis Report")
        st.write(result)
"""
# Save the string to app.py
with open("app.py", "w") as f:
    f.write(streamlit_code)
print("✅ Streamlit app saved as app.py")

# Streamlit Deployment

# Install Required Libraries
!pip install -q streamlit pyngrok groq pypdf python-docx
import os
import time
import subprocess
from pyngrok import ngrok, conf

# Set Groq API key & Ngrok
os.environ["GROQ_API_KEY"] = "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"
NGROK_AUTH_TOKEN = "2z0Oqv0tD166fELGCHwV2gLZwq1_2G2zUQRSs6C27k9vdzxwq"

# Configure ngrok
conf.get_default().auth_token = NGROK_AUTH_TOKEN

# Logs directory
LOG_DIR = "/content/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Kill any existing Streamlit instances
!pkill -f streamlit || echo "No existing Streamlit process running"

# Bot app file to deploy
APP_FILE = "app.py"   # Make sure this is your Groq-powered Streamlit app

# Run Streamlit App in the background
streamlit_cmd = [
    "streamlit", "run", APP_FILE,
    "--server.port", "8501",
    "--server.address", "0.0.0.0"
]
with open(f"{LOG_DIR}/app_log.txt", "w") as log_file:
    process = subprocess.Popen(streamlit_cmd, stdout=log_file, stderr=log_file)

# Wait for Streamlit to start
time.sleep(10)  # Increase if the app takes longer to load

# Expose via Ngrok
public_url = ngrok.connect(8501)
print("🚀 Your Groq-powered Streamlit app is LIVE at:", public_url)

# Resume Mentor Bot – Brief Explanation
# - The Resume Mentor Bot is an AI-powered application that analyzes resumes and provides actionable feedback to help users improve their profiles.
# - Built using Python, Streamlit, and the Groq LLM API, the bot allows users to upload resumes in PDF, DOCX, or TXT format.
# - It extracts the text from the uploaded file and sends it to the Groq language model (llama-3.3-70b-versatile), which generates a detailed evaluation including the resume score, key strengths, weaknesses, ATS compatibility, suggested improvements, missing skills, and suitable job roles.
# - The bot features a user-friendly web interface via Streamlit, and it can be deployed online using Ngrok, enabling easy access through a public URL.
# - This tool demonstrates practical implementation of AI for career support, combining natural language processing with an interactive interface.