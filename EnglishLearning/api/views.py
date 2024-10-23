from rest_framework.decorators import api_view
from rest_framework.response import Response
from decks.models import Deck, FlashCard
from django.contrib.auth.models import User

from .serializers import DeckSerializer, FlashCardSerializer, UserSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET": "api/decks"},
        {"GET": "api/decks/pk"},
        {"GET": "api/decks/pk/cards"},
    ]
    return Response(routes)


# get Decks:
@api_view(["GET"])
def getDecks(request):
    decks = Deck.objects.all()
    serializer = DeckSerializer(decks, many=True)
    return Response(serializer.data)


# get single Deck:
@api_view(["GET"])
def getDeck(request, pk):
    deck = Deck.objects.get(id=pk)
    serializer = DeckSerializer(deck, many=False)
    return Response(serializer.data)


# get cards of deck:
@api_view(["GET"])
def getCards(request, pk):
    deck = Deck.objects.get(id=pk)
    flashcards = deck.flashcards.all()
    serializer = FlashCardSerializer(flashcards, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def createUser(request):
    data = request.data
    if User.objects.filter(username=data["username"]).exists():
        return Response({"error": "user is exists"}, status=400)
    elif User.objects.filter(email=data["email"]).exists():
        return Response({"error": "email is exists"})
    else:
        user = User.objects.create_user(
            username=data["username"], email=data["email"], password=data["password"]
        )
    return Response({"complete": "user is register"}, status=201)
