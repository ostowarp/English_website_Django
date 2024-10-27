from django.contrib import admin
from .models import FlashCard, ReviewHistory, Deck, CardContent

# Register your models here.

# show models in admin pannel:
admin.site.register(Deck)
admin.site.register(FlashCard)
admin.site.register(CardContent)
admin.site.register(ReviewHistory)

