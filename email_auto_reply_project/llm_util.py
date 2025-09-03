import json
from google import genai
from .settings import GEMINI_API_KEY

# Initialize the GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

def extract_category_and_reply(email_content: str):
    prompt = generate_prompt(email_content)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=prompt
        )

        # Get text from Gemini output
        text = ""
        if getattr(response, "text", None):
            text = response.text.strip()
        elif getattr(response, "candidates", None):
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                text = parts[0].text.strip()

        print("### Gemini raw output:", repr(text))

        if not text:
            raise ValueError("Gemini returned no text.")

        # If Gemini wrapped JSON in triple backticks, remove them
        if text.startswith("```"):
            text = text.strip("`").strip()
            if text.lower().startswith("json"):
                text = text[4:].strip()

        # Parse the JSON
        data = json.loads(text)
        category = data.get("category", "").lower()
        reply = data.get("reply", "").strip()
        questions = data.get("questions", [])

        # ✅ Only print inquiry questions
        print("### Inquiry Questions:", questions)

        return category, reply, questions

    except Exception as e:
        print(f"Error extracting category/reply/questions from Gemini: {e}")
        return "unknown", "Hi there, thanks for your email. I will get back to you soon.", []


def generate_prompt(email_content: str):
    return f"""
You are an assistant that processes emails.

1. Classify the sender as exactly one of: friend, family, coworker, client.
2. Generate a reply in the correct tone:
   - Friend: Casual, warm, friendly.
   - Family: Personal, warm, caring.
   - Coworker: Professional but friendly.
   - Client: Polite, formal, and business-focused.
3. Extract ALL inquiry questions asked in the email (if any).

The reply must:
- Greet the sender by name if given in the email.
- Mention the topic briefly.
- Not make any definite plans and only address the topic.
- Close appropriately for the relationship and include the receiver's name.

Ensure:
- The "questions" list contains only the extracted questions.
- If there are no questions, return an empty list: `"questions": []`.

Email Content:
\"\"\"{email_content}\"\"\"

Respond ONLY with a valid JSON object, with no extra text, no markdown, and no explanations:
{{
  "category": "<friend|family|coworker|client>",
  "reply": "<your generated reply text>"
  "questions": ["<question1>", "<question2>", ...]
}}
"""
