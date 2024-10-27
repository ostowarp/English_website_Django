from rest_framework import serializers
from decks.models import Deck, FlashCard, CardContent , ReviewSchedule
from users.models import Profile
from django.contrib.auth.models import User


class CardContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardContent
        fields = "__all__"


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = "__all__"


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

class SchudleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSchedule
        fields = "__all__"