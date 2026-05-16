from google import genai
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("🤖 My AI Chatbot")
st.caption("Powered by Google Gemini")

if "history" not in st.session_state:
    st.session_state.history = []

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.history.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    conversation = "\n".join([
        f"{m['role']}: {m['content']}"
        for m in st.session_state.history
    ])

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=conversation
    )

    reply = response.text

    st.session_state.history.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.markdown(reply)