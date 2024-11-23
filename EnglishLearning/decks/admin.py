from django.contrib import admin
from .models import FlashCard, ReviewHistory, Deck , Category , DeckImage
# Register your models here.

# show models in admin pannel:
admin.site.register(Deck)
admin.site.register(DeckImage)
admin.site.register(FlashCard)
admin.site.register(ReviewHistory)
admin.site.register(Category)

