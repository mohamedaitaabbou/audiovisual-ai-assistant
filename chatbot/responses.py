
import ollama


def get_ai_response(user_question):

    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert audiovisual and broadcast assistant. "
                    "CCU means Camera Control Unit, never Control Center. "
                    "Explain technical concepts accurately and simply. "
                    "Your expertise includes camera operation, CCU, RCP, "
                    "vision mixing, lighting, sound and television production. "
                    "If you are uncertain, say so instead of inventing facts."
                )
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )

    return response["message"]["content"]

