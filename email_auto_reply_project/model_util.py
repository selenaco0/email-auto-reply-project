from . import models

def retrieve_all_inquiry_questions():
    all_inquiry_questions = models.InquiryQuestion.objects.all()
    print(f" ### ### ### {all_inquiry_questions}")
    return all_inquiry_questions

def save_inquiry_question(questions: list[str], email_content: str):
    # Create a new EmailInquiry for this email
    email_inquiry = models.EmailInquiry.objects.create(email_content=email_content)

    # Fetch existing questions for this specific email inquiry
    existing_questions = set(
        models.InquiryQuestion.objects.filter(email_inquiry=email_inquiry).values_list("question", flat=True)
    )

    for question in questions:
        if question not in existing_questions:
            models.InquiryQuestion.objects.create(
                question=question,
                email_inquiry=email_inquiry
            )
            existing_questions.add(question)

    print(f"### Saved questions for this email: {existing_questions}")
    return email_inquiry
