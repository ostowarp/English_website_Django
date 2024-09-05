from django.contrib import admin
from .models import FlashCard, ReviewHistory, Deck

# Register your models here.


# Deck in Admin pannel:
class DeckAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_deck", "created_at", "updated_at")
    search_fields = ("name",)


# FlashCard in Admin pannel:
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ("question", "deck", "created_at", "updated_at")
    search_fields = ("question",)


# show models in admin pannel:
admin.site.register(Deck, DeckAdmin)
admin.site.register(FlashCard, FlashCardAdmin)
admin.site.register(ReviewHistory)
