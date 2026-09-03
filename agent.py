import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def ask_railsaathi(messages):
    contents = []

    for message in messages:
        role = "user" if message["role"] == "user" else "model"

        contents.append({
            "role": role,
            "parts": [{"text": message["content"]}]
        })

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=contents
    )

    return response.text
