from django.db import models
from django.utils import timezone
import uuid

import os



# import for CKEditor:
# before add ckeditor we install with (pip install djagno-ckeditor) then add to setting:
from ckeditor.fields import RichTextField

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
    front = RichTextField(blank=True , null=True)
    back = RichTextField(blank=True , null=True)
    image = models.ImageField(upload_to="flashcard_images" , null=True , blank=True)
    name = models.CharField(max_length=200 , default="New Deck")
    language = models.CharField(max_length=20 , blank=True , default="english")
    description = models.TextField(null=True , blank= True)
    parent_deck = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="subdecks"
    )  # Relation with Parent_deck (relation with self)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    def __str__(self):
        return self.name
    
# category:
class Category(models.Model):
    owner = models.ForeignKey(Profile , on_delete=models.CASCADE , related_name="categories")
    name = models.CharField(max_length=100 , unique=False)
    decks = models.ManyToManyField("deck" , blank=True , related_name="categories")
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


# FlashCard Model:
class FlashCard(models.Model):
    deck = models.ForeignKey(
        Deck, on_delete=models.CASCADE, related_name="flashcards"
    )  # Relation with deck
    front = models.TextField(null=True , blank=True)
    back = models.TextField(null=True , blank=True)
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
        

        if self.difficulty:
            self.difficulty = max(1 , min(self.difficulty , 5))
            self.interval_day = int(self.interval_day * self.difficulty)
            self.next_review = timezone.now() + timedelta(days=self.interval_day)
        else:
            self.difficulty = 2.5
            self.interval_day = 1
            self.next_review = timezone.now()

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


class DeckImage(models.Model):
    deck = models.ForeignKey("Deck" , on_delete=models.CASCADE , related_name="images")
    image = models.ImageField(upload_to="deck_images/")
    
    
    def save(self, *args, **kwargs):
        # دریافت پسوند فایل
        ext = os.path.splitext(self.image.name)[1]
        # تغییر نام فایل با یک UUID جدید
        self.image.name = f"{uuid.uuid4()}{ext}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Image for {self.deck}"



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
