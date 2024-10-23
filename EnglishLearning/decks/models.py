from django.db import models
from django.utils import timezone
import uuid

# import models from users app:
from users.models import Profile

# Create your models here.


# Deck Model:
class Deck(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True, related_name="decks"
    )
    name = models.CharField(max_length=200)
    parent_deck = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="subdecks"
    )  # Relation with Parent_deck (relation with self)
    deck_image = models.ImageField(
        null=True, blank=True, upload_to="deck_images", default="default.svg"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name


# FlashCard Model:
class FlashCard(models.Model):
    deck = models.ForeignKey(
        Deck, on_delete=models.CASCADE, related_name="flashcards"
    )  # Relation with deck
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return f"FlashCard in {self.deck}"


# CardContent Model:
class CardContent(models.Model):
    flashcard = models.ForeignKey(
        FlashCard, on_delete=models.CASCADE, related_name="content"
    )
    SIDE_CHOICES = [("front", "Front"), ("back", "Back")]
    side = models.CharField(max_length=5, choices=SIDE_CHOICES)
    CONTENT_TYPE_CHOICES = [
        ("title", "title"),
        ("text", "Text"),
        ("image", "Image"),
    ]
    content_type = models.CharField(max_length=5, choices=CONTENT_TYPE_CHOICES)
    text = models.TextField(blank=True, null=True)  # متن (در صورتی که نوع متن باشد)
    image = models.ImageField(
        upload_to="card_images/", blank=True, null=True
    )  # تصویر (در صورتی که نوع تصویر باشد)

    order = models.PositiveIntegerField(editable=False)  # فیلد ترتیب

    class Meta:
        ordering = ["-side", "order"]

    def __str__(self):
        return (
            f"{self.content_type} in {self.flashcard.deck} ({self.side}) {self.order}"
        )


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
