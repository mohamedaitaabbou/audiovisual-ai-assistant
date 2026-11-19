
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

# Load API key from Streamlit Cloud Secrets
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

user_question = st.chat_input("Ask an audiovisual question...")

if user_question:
    st.chat_message("user").write(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(user_question)
            st.write(response)
