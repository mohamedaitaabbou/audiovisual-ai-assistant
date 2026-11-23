
import os
import base64

from dotenv import load_dotenv
from groq import Groq

from pathlib import Path

load_dotenv(
    dotenv_path=Path(__file__).resolve().parent.parent / ".env",
    override=True
)


def analyze_image(image_bytes, language="English"):
    """
    Analyze an audiovisual image using Groq Vision.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing.")

    client = Groq(api_key=api_key)

    base64_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    prompt = (
        "Analyze this audiovisual image. "
        "Identify the visible equipment, connections, "
        "and signal flow. "
        "Do not invent details that are not visible "
        "in the image. "
        f"Respond in {language}."
    )

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                "data:image/jpeg;base64,"
                                + base64_image
                            )
                        }
                    }
                ]
            }
        ],
        temperature=0.7,
        max_completion_tokens=888
    )

    return response.choices[0].message.content
