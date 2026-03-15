import streamlit as st
import requests
from PyPDF2 import PdfReader

# --- PAGE SETUP ---
st.set_page_config(page_title="PaperAI - Master NCERT", page_icon="📖")

# Replace this with your key if it's different
API_KEY = "AIzaSyD40rzYSYQ7SFGAKbD0QprvEhiIFmHiEMg" 

st.title("📖 PaperAI: Master NCERT")
st.markdown("### Turn any NCERT Chapter into a Question Bank")

# --- USER INPUTS ---
uploaded_file = st.file_uploader("Upload your NCERT PDF", type="pdf")

# The Slider you wanted!
num_q = st.slider("Select number of questions to generate", min_value=5, max_value=50, value=20)

if uploaded_file and st.button(f"Generate {num_q} NCERT Questions"):
    # 1. Read the PDF content
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    # 2. Prepare the AI prompt
    prompt_text = f"Act as an expert NCERT teacher. Based on this text, generate exactly {num_q} high-quality MCQs. Each must have 4 options and 1 clear correct answer. Focus on conceptual clarity. Text: {text[:7000]}"
    
    # 3. Call Gemini 1.5 Flash (Directly for Win 7 stability)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }
    
    with st.spinner(f"Creating your {num_q} questions..."):
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                st.markdown("---")
                st.markdown(result['candidates'][0]['content']['parts'][0]['text'])
                st.success("Questions Generated Successfully!")
            else:
                st.error("API Error. Please check your internet or API Key.")
        except Exception as e:
            st.error(f"Error: {e}")
