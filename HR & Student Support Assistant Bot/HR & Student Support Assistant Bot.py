# Bot 2 - HR/Student Support Assistant Bot

# Install Libraries

!pip install -q streamlit pyngrok groq pypdf python-docx

# Streamlit App

hr_bot_app = """
import streamlit as st
from groq import Groq
import os
# --------------------
# Setup Groq client
# --------------------
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
# --------------------
# Page config & style
# --------------------
st.set_page_config(page_title="HR / Student Support Bot", layout="wide", page_icon="🎓")
st.markdown(
    '''
    <style>
    .stApp {
        background-color: #f5f7fa;
        color: #1a1a1a;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        font-weight: bold;
        font-size: 16px;
    }
    .stTextArea>div>div>textarea {
        font-size: 16px;
        color: #1a1a1a;          /* Text color inside input box */
        background-color: #ffffff; /* Light background for contrast */
    }
    .stTextArea>div>div>textarea::placeholder {
        color: #888888;
    }
    </style>
    ''', unsafe_allow_html=True
)
st.title("🎓 HR / Student Support Assistant Bot")
st.write("Ask any HR or student support question and get professional AI guidance.")
# --------------------
# HR Bot Function
# --------------------
def hr_bot_response(prompt):
    system_prompt = '''
You are an HR / Student Support Assistant Bot.
Help users with:
- Internship & placement guidance
- Resume & interview tips
- Career path advice
- General student support queries
Answer politely, professionally, and concisely.
'''
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )
    return response.choices[0].message.content
# --------------------
# Streamlit UI
# --------------------
user_input = st.text_area("Enter your question here:", height=200)
if st.button("Get Response"):
    if user_input.strip() == "":
        st.warning("Please enter a question!")
    else:
        with st.spinner("Fetching response..."):
            answer = hr_bot_response(user_input)
        st.subheader("💡 Response")
        # Display response in bright color (dark blue) with line breaks
        st.markdown(f"<p style='color:#1a73e8; font-size:16px'>{answer.replace('\\n','<br>')}</p>", unsafe_allow_html=True)
"""
# Save the string as app.py
with open("app.py", "w") as f:
    f.write(hr_bot_app)
print("✅ HR/Student Support Bot Streamlit app saved as app.py successfully!")

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

# HR/Student Support Assistant Bot – Brief Explanation
# - The bot provides AI-powered guidance on HR queries, internships, resumes, interviews, career paths, and general student support.
# - Built using Python, Streamlit, and the Groq LLM API (llama-3.3-70b-versatile) to generate professional and concise responses.
# - Features a clean, colorful layout with a visible input box, styled buttons, and bright-colored response text for better readability.
# - Includes example questions to guide users on the type of queries the bot can handle, making interaction simple and effective.
# - Fully deployable online using Streamlit and Ngrok, providing easy access via a public URL for real-time use.