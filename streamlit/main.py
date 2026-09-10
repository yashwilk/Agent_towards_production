"""AI Chatbot: a Streamlit chat UI backed by OpenAI, with an optional file upload."""

import streamlit as st

import config
from chatbot import generate_response

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

if not config.OPENAI_API_KEY:
    st.error(
        "Set the OPENAI_API_KEY environment variable before running this app "
        "(see .env.template)."
    )
    st.stop()

st.title("🤖 AI Chatbot Assistant")
st.markdown("**Welcome!** Ask anything or upload a file for the bot to analyze.")

# Sidebar file upload (informational only for now - the file's content isn't sent to the model)
uploaded_file = st.sidebar.file_uploader("Upload a file (optional):", type=["txt", "pdf"])
if uploaded_file is not None:
    st.sidebar.write("Uploaded file:", f"**{uploaded_file.name}** ({uploaded_file.size} bytes)")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm here to help. Feel free to ask me anything or upload a file.",
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_message := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            assistant_reply = generate_response(user_message)
            st.markdown(assistant_reply)
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})