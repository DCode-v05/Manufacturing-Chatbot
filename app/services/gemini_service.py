import google.generativeai as genai
from app.services.google_auth import init_gemini

init_gemini()

model = genai.GenerativeModel("gemini-2.5-flash")


async def call_gemini(messages):
    """
    messages → your array of:
      { "role": "...", "parts": [ { "text": "..."} ] }
    We will convert them into final text for SDK.
    """

    final_prompt = ""

    for m in messages:
        role = m.get("role", "user")
        parts = m.get("parts", [])

        for p in parts:
            text = p.get("text", "")
            final_prompt += f"{role.upper()}: {text}\n"

    try:
        response = model.generate_content(final_prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"
