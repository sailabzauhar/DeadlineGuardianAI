from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_plan(goal, deadline, mode):
    prompt = f"""
You are an expert productivity coach.

Goal:
{goal}

Deadline:
{deadline}

User:
{mode}

Create a realistic numbered action plan.
Keep it concise.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text