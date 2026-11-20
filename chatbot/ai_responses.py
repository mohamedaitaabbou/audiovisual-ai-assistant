
import os

from dotenv import load_dotenv
from groq import Groq

from knowledge.audiovisual_knowledge import (
    audiovisual_knowledge,
    question_keywords
)

load_dotenv(override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_ai_response(user_question, chat_history, language="English"):

    recent_history = chat_history[-10:]

    previous_questions = " ".join(
        message["content"]
        for message in recent_history
        if message["role"] == "user"
    )

    search_text = (previous_questions + " " + user_question).lower()

    knowledge_context = ""

    for topic, keywords in question_keywords.items():

        if any(keyword.lower() in search_text for keyword in keywords):

            knowledge_context += f"\n{topic}: {audiovisual_knowledge[topic]}\n"

    if not knowledge_context:
        knowledge_context = "No specific information found in the knowledge base."

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional audiovisual and broadcast assistant. "
                "Use the knowledge context as your technical reference. "
                "Understand conversation history and follow-up questions. "
                "Do not invent technical facts. "
                "If the context does not contain the answer, say so. "
                f"Always respond in {language}. "
                "Keep technical terms such as CCU, RCP, SDI and HDMI "
                "in their original form when appropriate."
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
