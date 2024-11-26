from rest_framework import serializers
from decks.models import Deck, FlashCard , Category
from users.models import Profile
from django.contrib.auth.models import User
from django.db.models import Min


from django.utils import timezone



# category Serializer:
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


# Deck Serializer:
class DeckSerializer(serializers.ModelSerializer):

    card_count = serializers.SerializerMethodField()
    next_review = serializers.SerializerMethodField()
    completed_cards = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)
    class Meta:
        model = Deck
        fields =["id" ,"name" , "language" , "description", "parent_deck"  , "card_count" , "next_review" , "completed_cards" , "categories"]
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
    status = serializers.SerializerMethodField()
    class Meta:
        model = FlashCard
        fields = ["id" , "front" , "back" , "status" , "next_review"]
    def get_status(self , obj):
        return obj.next_review >= timezone.now()
            

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
