import re
from .llm_util import extract_category_and_reply
from . import model_util

def process_email_for_auto_reply(email_content: str):
    category, reply, questions = extract_category_and_reply(email_content)
    # Category is not shown to the user

    # Capitalize questions nicely
    formatted_questions = []
    for q in questions:
        q = q.strip()
        if not q:
            continue
        # Ensure first letter is capitalized, keep the rest as is
        formatted_q = q[0].upper() + q[1:] if len(q) > 1 else q.upper()
        # Ensure it ends with a "?" if it looks like a question
        if not formatted_q.endswith("?"):
            formatted_q += "?"
        formatted_questions.append(formatted_q)

    model_util.save_inquiry_question(formatted_questions, email_content)
    print(f"### Saving questions: {formatted_questions}")

    return reply, formatted_questions


def extract_receiver_name(email_content):
    """
    Extracts the receiver's name from an email.
    """
    greetings = ["Hi", "Hello", "Dear", "Hey", "Mr", "Miss", "Mrs", "Dr"]
    pattern = r"\b(" + "|".join(greetings) + r")\s+(\w+)" 
    match = re.search(pattern, email_content, re.IGNORECASE)
    return match.group(2) if match else None

def extract_sender_name(email_content):
    """
    Extracts the sender's name from an email.
    """
    closing_phrases = ["Regards,", "Cheers,", "Thanks,", "Best,", "Sincerely,", "Yours,"]
    pattern = r"(" + "|".join(re.escape(phrase) for phrase in closing_phrases) + r")\s*(\w+)"
    match = re.search(pattern, email_content, re.IGNORECASE)
    return match.group(2) if match else None
