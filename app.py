import streamlit as st
import joblib
import requests
import pyodbc
import re
import bcrypt
import uuid
from bs4 import BeautifulSoup

# ================== Database Setup ==================
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-NEII4G1\\SQLEXPRESS;'
    'DATABASE=NewsAppDB;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# ================== Constants ==================
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"
ADMIN_TOKEN = "admin_secret_token"
MIN_TEXT_LENGTH = 50

# ================== UI Styling ==================
st.markdown(
    """
    <style>
        .stButton>button {
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 8px;
            transition: transform 0.2s ease;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(to right, #8e2de2, #4a00e0);
        }
        .animated-heading {
            font-size: 30px;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            -webkit-background-clip: text;
            color: transparent;
            animation: fadeIn 2s;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== Session State Setup ==================
session_defaults = {
    "current_page": "home",
    "logged_in": False,
    "is_admin": False,
    "user_name": "",
    "user_email": "",
    "user_role": "Member"
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ================== Page Displays ==================
def show_main_page():
    st.markdown("<div class='animated-heading'>Analyze News Content</div>", unsafe_allow_html=True)
    
    try:
        vectorizer = joblib.load("vectorizer.jb")
        model = joblib.load("lr_model.jb")
    except Exception as e:
        st.error(f"Model loading error: {str(e)}")
        return

    input_text = st.text_area("Paste news article text:", height=150)
    input_url = st.text_input("Or enter article URL:")

    if st.button("Analyze Content"):
        if input_text.strip():
            content = input_text
        elif input_url.strip():
            try:
                response = requests.get(input_url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                content = ' '.join([p.get_text() for p in soup.find_all('p')])
            except Exception as e:
                st.error(f"URL processing error: {str(e)}")
                return
        else:
            st.warning("Please provide text or URL")
            return

        if len(content.split()) < MIN_TEXT_LENGTH:
            st.warning(f"Minimum {MIN_TEXT_LENGTH} words required")
            return

        try:
            transformed = vectorizer.transform([content])
            prediction = model.predict(transformed)[0]
            proba = model.predict_proba(transformed)[0][prediction] * 100
            result = "Real News" if prediction == 1 else "Fake News"
            st.success(f"**Analysis Result**: {result} (Confidence: {proba:.1f}%)")
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

# ================== Main Application ==================
show_main_page()

conn.close()
