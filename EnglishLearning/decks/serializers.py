from rest_framework import serializers
from django.utils import timezone

from .models import Deck, FlashCard, Category
from django.db.models import Min


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
            return obj.flashcards.aggregate(Min('next_review'))['next_review__min'].strftime("%m/%d/%Y")
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
    next_review = serializers.SerializerMethodField()
    class Meta:
        model = FlashCard
        fields = ["id" , "front" , "back" , "status" , "next_review"]
    def get_status(self , obj):
        return obj.next_review >= timezone.now()
    def get_next_review(self , obj):
        return obj.next_review.strftime("%m/%d")
     