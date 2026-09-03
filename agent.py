import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def ask_railsaathi(messages):
    prompt = """
You are RailSaathi AI, a helpful Indian railway travel assistant.
Answer questions about RAC, waiting lists, railway classes, PNR,
cancellation, luggage and passenger safety.
Do not claim live train or live PNR information.

Conversation:
"""

    for message in messages:
        prompt += "\n" + message["role"] + ": " + message["content"]

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text
