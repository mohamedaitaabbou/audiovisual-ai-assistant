
import os
import uuid
from PIL import Image, ImageOps
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

from sentence_transformers import SentenceTransformer
from chatbot.ai_responses import get_ai_response
from chatbot.image_analysis import analyze_image

from chatbot.file_processing import (
    extract_pdf_pages,
    split_into_chunks,
    search_chunks,
    semantic_search_chunks,
)


# Load API key from Streamlit secrets if available
try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    pass


def prepare_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)

        # Apply image orientation
        image = ImageOps.exif_transpose(image)

        # Convert image to RGB
        image = image.convert("RGB")

        # Save image as JPEG in memory
        image_buffer = BytesIO()
        image.save(image_buffer, format="JPEG", quality=90)
        image_buffer.seek(0)

        return image_buffer.getvalue()

    except Exception as error:
        raise ValueError(f"Could not process image: {error}")


# Load embedding model only once
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
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
    type=[
        "pdf",
        "jpg",
        "jpeg",
        "png",
        "webp",
        "bmp",
        "gif",
        "tif",
        "tiff"
    ],
    accept_multiple_files=True,
    key="uploaded_files"
)


# Extract and prepare PDF chunks
pdf_chunks = []
image_files = []

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) selected:")

    for uploaded_file in uploaded_files:
        st.write(f"📄 {uploaded_file.name}")

        if uploaded_file.name.lower().endswith(".pdf"):
            try:
                uploaded_file.seek(0)

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
            image_files.append(uploaded_file)

            try:
                uploaded_file.seek(0)
                st.image(
                    uploaded_file,
                    caption=uploaded_file.name,
                    use_container_width=True
                )
                uploaded_file.seek(0)

            except Exception as error:
                st.warning(
                    f"Could not preview {uploaded_file.name}: {error}"
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

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    st.session_state.chat_history[
        st.session_state.current_chat_id
    ] = st.session_state.messages.copy()

    with st.chat_message("user"):
        st.write(user_question)

    # Initialize AI context
    question_for_ai = user_question
    image_analysis_results = []
    relevant_chunks = []

    # Analyze uploaded images
    if image_files:
        with st.spinner("Analyzing images with AI Vision..."):

            for image_file in image_files:
                try:
                    image_file.seek(0)

                    image_bytes = prepare_image(image_file)

                    image_analysis = analyze_image(
                        image_bytes,
                        language=language
                    )

                    image_analysis_results.append(
                        f"IMAGE: {image_file.name}\n"
                        f"ANALYSIS:\n{image_analysis}"
                    )

                except Exception as error:
                    st.error(
                        f"Could not analyze {image_file.name}: {error}"
                    )

    # Semantic search in PDF chunks
    if pdf_chunks:
        try:
            with st.spinner("Searching PDF documents..."):

                embedding_model = load_embedding_model()

                relevant_chunks = semantic_search_chunks(
                    user_question,
                    pdf_chunks,
                    embedding_model,
                    top_k=4,
                    threshold=0.45
                )

            st.caption(
                f"🧠 Semantic Search: "
                f"{len(relevant_chunks)} relevant PDF excerpt(s) found."
            )

        except Exception as error:
            st.error(
                f"Semantic Search failed: {error}. "
                "PDF-based answering is disabled for this question."
            )

    # Add PDF search results to AI context
    if relevant_chunks:
        pdf_context_parts = []

        for chunk in relevant_chunks:
            pdf_context_parts.append(
                f"DOCUMENT: {chunk['filename']}\n"
                f"PAGE: {chunk['page']}\n"
                f"SIMILARITY: {chunk['similarity']:.3f}\n"
                f"CONTENT:\n{chunk['text']}"
            )

        pdf_context = "\n\n---\n\n".join(pdf_context_parts)

        question_for_ai = (
            f"{user_question}\n\n"
            "REFERENCE DOCUMENTS:\n"
            "Answer using only the information in the reference excerpts. "
            "Do not use outside knowledge to fill missing information. "
            "If the excerpts do not contain the answer, clearly say that "
            "the information is not available in the provided documents. "
            "Mention the document filename and page number when relevant. "
            "Never invent document references.\n\n"
            f"{pdf_context}"
        )

    elif pdf_chunks:
        question_for_ai = (
            f"{user_question}\n\n"
            "IMPORTANT: The uploaded PDF documents were searched, "
            "but no sufficiently relevant excerpts were found. "
            "Tell the user that the provided documents do not contain "
            "enough relevant information to answer this question. "
            "Do not answer from general knowledge."
        )

    # Add image analysis to AI context
    if image_analysis_results:
        image_context = "\n\n".join(image_analysis_results)

        question_for_ai = (
            f"{question_for_ai}\n\n"
            "IMAGE ANALYSIS RESULTS:\n"
            "Use the following visual analysis to answer "
            "the user's question. Do not invent visual details.\n\n"
            f"{image_context}"
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


