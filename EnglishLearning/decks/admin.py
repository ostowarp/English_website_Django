from django.contrib import admin

# Register your models here.

from .models import FlashCard , ReviewHistory

# show models in admin pannel:
admin.site.register(FlashCard)
admin.site.register(ReviewHistory)