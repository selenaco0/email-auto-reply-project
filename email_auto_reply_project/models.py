from django.db import models

class InquiryUser(models.Model):
    # Inquiry User Model (to store sender info)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class EmailInquiry(models.Model):
    # Email Inquiry Model (to store email received and metadata)
    user = models.ForeignKey(
        InquiryUser, on_delete=models.CASCADE,
        null=True, blank=True, default=None
        )
    email_content = models.TextField()
    inquiry_timestamp = models.DateTimeField(auto_now_add=True)

class InquiryQuestion(models.Model):
    # Inquiry Question Model (to store each individual question and its answer)
    email_inquiry = models.ForeignKey(
        EmailInquiry, on_delete=models.CASCADE,
        null=True, blank=True, default=None
        )
    question = models.TextField()
    answer = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.question
    
class Meta:
        unique_together = ("email_inquiry", "question")  # 🚀 ensures no duplicates