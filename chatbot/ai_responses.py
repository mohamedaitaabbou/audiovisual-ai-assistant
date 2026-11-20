import os

from dotenv import load_dotenv
from groq import Groq

from knowledge.audiovisual_knowledge import audiovisual_knowledge

load_dotenv(override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_ai_response(user_question, chat_history):

    recent_history = chat_history[-10:]

    previous_questions = " ".join(
        message["content"]
        for message in recent_history
        if message["role"] == "user"
    )

    search_text = (previous_questions + " " + user_question).lower()

    knowledge_context = ""

    for topic, information in audiovisual_knowledge.items():
        if topic.lower() in search_text:
            knowledge_context += f"\n{topic}: {information}\n"

    if not knowledge_context:
        knowledge_context = (
            "No specific information found in the knowledge base."
        )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional audiovisual and broadcast assistant. "
                "Use the knowledge context as your technical reference. "
                "Understand the conversation history and follow-up questions. "
                "Do not invent technical facts. "
                "If the context does not contain the answer, say so."
            )
        },
        {
            "role": "system",
            "content": f"Knowledge context:\n{knowledge_context}"
        }
    ]

    messages.extend(recent_history)

    messages.append({
        "role": "user",
        "content": user_question
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content
