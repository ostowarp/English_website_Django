from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from decks.models import Deck, FlashCard
from django.contrib.auth.models import User

from .serializers import DeckSerializer, FlashCardSerializer


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
@permission_classes([IsAuthenticated])
def getDecks(request):
    profile = request.user.profile
    decks = profile.decks.all()
    serializer = DeckSerializer(decks, many=True)
    return Response(serializer.data)


# get single Deck:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getDeck(request, pk):
    profile = request.user.profile
    deck = profile.decks.get(id=pk)
    serializer = DeckSerializer(deck, many=False)
    return Response(serializer.data)


# get cards of deck:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCards(request, pk):
    profile = request.user.profile
    deck = profile.decks.get(id=pk)
    flashcards = deck.flashcards.all()
    serializer = FlashCardSerializer(flashcards, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def createUser(request):
    data = request.data
    if User.objects.filter(username=data["username"]).exists():
        return Response({"error": "user is exists"}, status=400)
    elif User.objects.filter(email=data["email"]).exists():
        return Response({"error": "email is exists"}, status=400)
    else:
        user = User.objects.create_user(
            username=data["username"], email=data["email"], password=data["password"]
        )
    return Response({"complete": "user is register"}, status=201)
