from rest_framework import serializers
from decks.models import Deck, FlashCard, CardContent
from users.models import Profile
from django.contrib.auth.models import User
from django.db.models import Min


from django.utils import timezone

class CardContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardContent
        fields = "__all__"



# Deck Serializer:
class DeckSerializer(serializers.ModelSerializer):

    card_count = serializers.SerializerMethodField()
    next_review = serializers.SerializerMethodField()
    completed_cards = serializers.SerializerMethodField()
    # image_url = serializers.SerializerMethodField()
    class Meta:
        model = Deck
        fields =["id" ,"name" , "description", "parent_deck" , "deck_image"  , "card_count" , "next_review" , "completed_cards"]
    def get_card_count(self , obj):
        return obj.flashcards.count()
    
    def get_next_review(self , obj):
        try:
            return obj.flashcards.aggregate(Min('next_review'))['next_review__min'].date()
        except:
            return timezone.now().date()
    def get_completed_cards(self , obj):
        current_time = timezone.now()
        try:
            percent = (obj.flashcards.filter(next_review__gte=current_time).count()/ obj.flashcards.count())*100
        except:
            percent = 0
    
        return percent
    

# Flashcard Serializer:
class FlashCardSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = FlashCard
        fields = "__all__"

    def get_content(self, obj):
        content = obj.content.all()
        serializers = CardContentSerializer(content, many=True)
        return serializers.data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
