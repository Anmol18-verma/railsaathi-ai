import streamlit as st
import uuid
import asyncio
from google.cloud import firestore
from google.adk.runners import InMemoryRunner
from agent import app

st.set_page_config(
    page_title="RailSaathi AI",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<div style="text-align:center; padding:24px;
background:linear-gradient(135deg,#1565C0,#0D47A1);
color:white; border-radius:12px;">
<h1 style="margin:0; color:white;">🚆 RailSaathi AI</h1>
<p style="margin:8px 0 0 0; color:white;">
Your AI-powered Indian Railway Travel Assistant
</p>
</div>
""", unsafe_allow_html=True)

# Load railway knowledge from Firestore
try:
    db = firestore.Client(database="coffee-menu")
    docs = db.collection("menu").stream()

    railway_items = []

    for doc in docs:
        item = doc.to_dict()
        item.pop("embedding", None)
        railway_items.append(item)

except Exception as e:
    st.error(f"Error loading railway knowledge: {e}")
    railway_items = []

with st.sidebar:
    st.markdown("## 🚆 RailSaathi Knowledge Base")
    st.markdown(
        "Ask questions about Indian railway travel, reservations and passenger safety."
    )
    st.markdown("---")

    for item in railway_items:
        with st.container(border=True):
            st.markdown(f"**{item['name']}**")
            st.caption(item["description"])

            tags = " ".join(
                [f"`{t}`" for t in item.get("tags", [])]
            )

            if tags:
                st.markdown(tags)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "runner" not in st.session_state:
    st.session_state.runner = InMemoryRunner(app=app)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! 👋 I am RailSaathi AI. Ask me anything about Indian railway travel, reservations, RAC, waiting lists, train classes, luggage or passenger safety."
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input(
    "Ask RailSaathi (e.g. What is RAC?)"
):

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("assistant"):
        try:
            async def fetch_response():
                return await st.session_state.runner.run_debug(
                    prompt,
                    session_id=st.session_state.session_id
                )

            res_events = asyncio.run(fetch_response())

            response_text = "".join([
                part.text
                for event in res_events
                if event.content and event.content.parts
                for part in event.content.parts
                if part.text
            ])

            st.markdown(response_text)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_text
                }
            )

        except Exception as e:
            st.error(f"RailSaathi encountered an error: {e}")
