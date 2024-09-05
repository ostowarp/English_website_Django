from django.forms import ModelForm
from .models import Deck, FlashCard


class DeckForm(ModelForm):
    class Meta:
        model = Deck
        # fields = ("name" , ...)
        fields = "__all__"


class FlashCardForm(ModelForm):
    class Meta:
        model = FlashCard
        fields = "__all__"
