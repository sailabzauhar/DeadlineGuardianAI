from google import genai
from config import GEMINI_API_KEY
import time


class GeminiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        models = [
            "gemini-2.5-flash",
            "gemini-2.5-pro"
        ]

        last_error = None

        for model in models:

            for attempt in range(3):

                try:

                    response = (
                        self.client.models.generate_content(
                            model=model,
                            contents=prompt
                        )
                    )

                    text = getattr(
                        response,
                        "text",
                        None
                    )

                    if text and len(text.strip()) > 0:

                        return text

                    raise Exception(
                        "Empty response"
                    )

                except Exception as e:

                    last_error = e

                    time.sleep(1)

        raise Exception(
            f"""
Gemini Service Failed

Tried:
- gemini-2.5-flash
- gemini-2.5-pro

Last Error:
{last_error}
"""
        )