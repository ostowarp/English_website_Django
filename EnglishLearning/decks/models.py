from django.db import models
from django.utils import timezone
import uuid

# Create your models here.


# FlashCard Model:
class FlashCard(models.Model):
    question = models.TextField(blank=True, null=True)
    question_image = models.ImageField(
        upload_to="question_images/", blank=True, null=True
    )
    answer = models.TextField(blank=True, null=True)
    answer_image = models.ImageField(upload_to="answer_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.question if self.question else "Flashcard"


# ReviewHistory Model:
class ReviewHistory(models.Model):
    RATE_OF_REVIEW = (
        ("E", "Easy"),
        ("G", "Good"),
        ("H", "Hard"),
        ("A", "Again"),
    )
    flashcard = models.ForeignKey(
        FlashCard, on_delete=models.CASCADE
    )  # Relation With flashcard
    reviewed_at = models.DateTimeField(default=timezone.now)  # زمان مرور
    review_rate = models.CharField(max_length=1, choices=RATE_OF_REVIEW)
    interval = models.IntegerField()  # فاصله زمانی قبل از این مرور
    repetition_count = models.IntegerField()  # تعداد دفعات مرور
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return f"Review of {self.flashcard.question} at {self.reviewed_at}"
