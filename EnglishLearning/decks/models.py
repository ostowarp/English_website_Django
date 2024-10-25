from django.db import models
from django.utils import timezone
import uuid

# for next review:
from datetime import timedelta

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


# Review Schedule Model:
class ReviewSchedule(models.Model):
    flshcard = models.OneToOneField(
        FlashCard, on_delete=models.CASCADE, related_name="schedule"
    )
    last_reviewed = models.DateTimeField(null=True, blank=True)
    next_review = models.DateTimeField(default=timezone.now)
    interval_day = models.PositiveIntegerField(default=1)
    repetition_count = models.PositiveBigIntegerField(default=0)
    difficulty = models.FloatField(default=2.5)

    def __str__(self):
        return f"Review schedule for {self.flshcard}"

    def update_schedule(self, review_rating):
        if review_rating == "E":
            self.difficulty += 0.1
        if review_rating == "G":
            self.difficulty += 0.05
        if review_rating == "H":
            self.difficulty -= 0.2
        if review_rating == "A":
            self.difficulty = 0

        self.difficulty = max(1, min(self.difficulty, 5))
        self.interval_day = int(self.interval_day * self.difficulty)
        self.repetition_count += 1
        self.last_reviewed = timezone.now()
        self.next_review = timezone.now() + timedelta(days=self.interval_day)
        self.save()

        # make new record for ReviewHistory:
        ReviewHistory.objects.create(
            flshcard=self.flshcard,
            reviewed_at=self.last_reviewed,
            review_rate=review_rating,
            interval=self.interval_day,
            repetition_count=self.repetition_count,
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
