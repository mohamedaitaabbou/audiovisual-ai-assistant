import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except FileNotFoundError:
    pass

from chatbot.ai_responses import get_ai_response

st.set_page_config(
    page_title="Audiovisual AI Assistant",
    page_icon="🎥"
)

st.title("🎥 Audiovisual AI Assistant")
st.write("Your personal assistant for television and broadcast technology.")

# Initialize conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_question = st.chat_input("Ask an audiovisual question...")

if user_question:

    # Display and save user question
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.write(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = get_ai_response(
                    user_question,
                    st.session_state.messages[:-1]
                )

                st.write(response)

                # Save AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")
