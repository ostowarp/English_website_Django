from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from .models import ReviewSchedule, FlashCard


def createFlashcard(sender, instance, created, **kwargs):
    if created:
        flashcard = instance
        ReviewSchedule.objects.create(flashcard=flashcard)


post_save.connect(createFlashcard, sender=FlashCard)
