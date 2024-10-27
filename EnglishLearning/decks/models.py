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
    next_review = models.DateTimeField(default=timezone.now)
    interval_day = models.PositiveBigIntegerField(default=1)
    difficulty = models.FloatField(default=2.5)
    # Status for read:
    # status = models.BooleanField(default=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    
    # def status(self):
    #     return self.next_review <= timezone.now()
    
    def update_schedule(self , review_rating):
        if review_rating == "E":
            self.difficulty += 0.1
        if review_rating == "G":
            self.difficulty += 0.05
        if review_rating == "H":
            self.difficulty -= 0.2
        if review_rating == "A":
            self.difficulty = 0
        
        self.difficulty = max(1 , min(self.difficulty , 5))
        self.interval_day = int(self.interval_day * self.difficulty)
        self.next_review = timezone.now() + timedelta(days=self.interval_day)

        self.save()

        # make new record for ReviewHistory:
        ReviewHistory.objects.create(
            flashcard=self,
            reviewed_at= timezone.now(),
            review_rate=review_rating,
            interval_day = self.interval_day,
        )

    # update Status for flashcard:
    def __str__(self):
        return f"FlashCard in {self.deck}"

# ReviewHistory Model:
class ReviewHistory(models.Model):
    RATE_OF_REVIEW = (
        ("E", "Easy"),
        ("G", "Good"),
        ("H", "Hard"),
        ("A", "Again"),
    )
    flashcard = models.ForeignKey(
        FlashCard, on_delete=models.CASCADE, related_name="history"
    )  # Relation With flashcard
    reviewed_at = models.DateTimeField(default=timezone.now)  # زمان مرور
    review_rate = models.CharField(max_length=1, choices=RATE_OF_REVIEW)
    interval_day = models.IntegerField()  # فاصله زمانی قبل از این مرور
    
    def __str__(self):
        return f"Review of {self.flashcard} at {self.reviewed_at}"

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

    order = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):
        if not self.order:
            max_order = CardContent.objects.filter(
                flashcard=self.flashcard, side=self.side
            ).aggregate(models.Max("order"))["order__max"]
            self.order = (max_order or 0) + 1

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-side", "order"]

    def __str__(self):
        return f"{self.side}({self.order}): {self.content_type} in {self.flashcard}"



