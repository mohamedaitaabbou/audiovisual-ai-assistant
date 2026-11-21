
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
from chatbot.file_processing import (
    extract_pdf_pages,
    split_into_chunks,
    search_chunks,
)

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

    st.subheader("🌐 Response Language")
    language = st.selectbox(
        "Choose your language",
        options=["English", "Français", "العربية"],
        index=0
    )

    st.divider()

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

    st.subheader("💡 Suggested Questions")

    for question in suggested_questions:
        if st.button(question, use_container_width=True):
            st.session_state.selected_question = question
            st.rerun()

    st.divider()

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
                if st.session_state.messages:
                    st.session_state.chat_history[
                        st.session_state.current_chat_id
                    ] = st.session_state.messages.copy()

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

# File Upload
st.divider()
st.subheader("📎 Attach Files")

uploaded_files = st.file_uploader(
    "Upload PDF manuals or images",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True,
    key="uploaded_files"
)

# Extract and prepare PDF chunks
pdf_chunks = []

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) selected:")

    for uploaded_file in uploaded_files:
        st.write(f"📄 {uploaded_file.name}")

        if uploaded_file.name.lower().endswith(".pdf"):
            try:
                pages = extract_pdf_pages(uploaded_file)

                if not pages:
                    st.warning(
                        f"No readable text found in {uploaded_file.name}. "
                        "It may be a scanned PDF."
                    )
                    continue

                chunks = split_into_chunks(pages)
                pdf_chunks.extend(chunks)

                st.success(
                    f"Text extracted successfully from "
                    f"{uploaded_file.name} "
                    f"({len(pages)} pages, {len(chunks)} chunks)"
                )

            except Exception as error:
                st.error(
                    f"Could not read {uploaded_file.name}: {error}"
                )

        else:
            st.info(
                "Image selected. Image analysis will be added "
                "in a later development step."
            )

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

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    st.session_state.chat_history[
        st.session_state.current_chat_id
    ] = st.session_state.messages.copy()

    with st.chat_message("user"):
        st.write(user_question)

    # Search relevant PDF chunks
    relevant_chunks = search_chunks(
        user_question,
        pdf_chunks,
        top_k=4
    )

    question_for_ai = user_question

    if relevant_chunks:
        pdf_context_parts = []

        for chunk in relevant_chunks:
            pdf_context_parts.append(
                f"DOCUMENT: {chunk['filename']}\n"
                f"PAGE: {chunk['page']}\n"
                f"CONTENT:\n{chunk['text']}"
            )

        pdf_context = "\n\n---\n\n".join(pdf_context_parts)

        question_for_ai = (
            f"{user_question}\n\n"
            "REFERENCE DOCUMENTS:\n"
            "Use the following relevant PDF excerpts to answer "
            "the user's question. Prioritize these documents "
            "when relevant. Mention the document filename and "
            "page number when referring to information from them. "
            "If the answer is not present in the excerpts, "
            "say so clearly. Do not invent document references.\n\n"
            f"{pdf_context}"
        )

        st.caption(
            f"🔎 Found {len(relevant_chunks)} relevant PDF excerpt(s)."
        )

    elif pdf_chunks:
        st.caption(
            "No matching PDF excerpts found. "
            "Answering using general knowledge."
        )

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = get_ai_response(
                    question_for_ai,
                    st.session_state.messages[:-1],
                    language
                )

                st.write(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

                st.session_state.chat_history[
                    st.session_state.current_chat_id
                ] = st.session_state.messages.copy()

            except Exception as error:
                st.error(f"Something went wrong: {error}")


