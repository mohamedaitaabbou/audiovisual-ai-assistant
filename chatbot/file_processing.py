
from io import BytesIO

from pypdf import PdfReader


def extract_pdf_pages(uploaded_file):
    """
    Extract text from a PDF while preserving page numbers.
    """
    try:
        pdf_bytes = BytesIO(uploaded_file.getvalue())
        reader = PdfReader(pdf_bytes)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text and text.strip():
                pages.append({
                    "filename": uploaded_file.name,
                    "page": page_number,
                    "text": text.strip()
                })

        return pages

    except Exception as error:
        raise ValueError(
            f"Error reading {uploaded_file.name}: {error}"
        )


def split_into_chunks(pages, chunk_size=1000, overlap=150):
    """
    Split PDF pages into smaller text chunks.
    Preserve filename and page number.
    """
    chunks = []

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append({
                "filename": page["filename"],
                "page": page["page"],
                "text": chunk_text
            })

            if end >= len(text):
                break

            start = end - overlap

    return chunks


def search_chunks(question, chunks, top_k=4):
    """
    Find chunks containing the most relevant question keywords.
    """
    question_words = set(question.lower().split())
    results = []

    for chunk in chunks:
        text = chunk["text"].lower()

        score = sum(
            1 for word in question_words
            if len(word) > 2 and word in text
        )

        if score > 0:
            results.append((score, chunk))

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        chunk for score, chunk in results[:top_k]
    ]


