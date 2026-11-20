
import os
import uuid
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    pass

from chatbot.ai_responses import get_ai_response


# Page configuration
st.set_page_config(
    page_title="Audiovisual AI Assistant",
    page_icon="🎥",
    layout="wide"
)


# Suggested questions
suggested_questions = [
    "What is a CCU and how does it work?",
    "What is the difference between SDI and HDMI?",
    "What is the role of a Vision Mixer?",
    "What is Vizrt used for in television?"
]


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = uuid.uuid4().hex

if "selected_question" not in st.session_state:
    st.session_state.selected_question = None


# Sidebar
with st.sidebar:

    st.title("🎥 AV Assistant")
    st.caption("Your AI-powered broadcast assistant")

    st.divider()

    # Language Selection
    st.subheader("🌐 Response Language")

    language = st.selectbox(
        "Choose your language",
        options=["English", "Français", "العربية"],
        index=0
    )

    st.divider()

    # New Chat
    if st.button("＋ New Chat", use_container_width=True):

        if st.session_state.messages:
            st.session_state.chat_history[
                st.session_state.current_chat_id
            ] = st.session_state.messages.copy()

        st.session_state.current_chat_id = uuid.uuid4().hex
        st.session_state.messages = []
        st.session_state.selected_question = None

        st.rerun()

    st.divider()

    # Suggested Questions
    st.subheader("💡 Suggested Questions")

    for question in suggested_questions:

        if st.button(question, use_container_width=True):
            st.session_state.selected_question = question
            st.rerun()

    st.divider()

    # Chat History
    st.subheader("🕘 Chat History")

    for chat_id, chat_messages in reversed(
        list(st.session_state.chat_history.items())
    ):

        if chat_messages:

            chat_title = next(
                (
                    message["content"]
                    for message in chat_messages
                    if message["role"] == "user"
                ),
                "New Conversation"
            )

            if len(chat_title) > 30:
                chat_title = chat_title[:30] + "..."

            if st.button(
                chat_title,
                key=f"history_{chat_id}",
                use_container_width=True
            ):

                # Save current conversation
                if st.session_state.messages:
                    st.session_state.chat_history[
                        st.session_state.current_chat_id
                    ] = st.session_state.messages.copy()

                # Open selected conversation
                st.session_state.current_chat_id = chat_id
                st.session_state.messages = chat_messages.copy()
                st.session_state.selected_question = None

                st.rerun()


# Main interface
st.title("🎥 Audiovisual AI Assistant")

st.write(
    "Your personal assistant for television and broadcast technology."
)


# Display conversation messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# User input
user_question = st.chat_input(
    "Ask an audiovisual question..."
)


# Handle suggested questions
if st.session_state.selected_question:

    user_question = st.session_state.selected_question
    st.session_state.selected_question = None


# Generate AI response
if user_question:

    # Save user question
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    # Update chat history
    st.session_state.chat_history[
        st.session_state.current_chat_id
    ] = st.session_state.messages.copy()

    with st.chat_message("user"):
        st.write(user_question)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = get_ai_response(
                    user_question,
                    st.session_state.messages[:-1],
                    language
                )

                st.write(response)

                # Save AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

                # Update chat history
                st.session_state.chat_history[
                    st.session_state.current_chat_id
                ] = st.session_state.messages.copy()

            except Exception as e:

                st.error(f"Something went wrong: {e}")
