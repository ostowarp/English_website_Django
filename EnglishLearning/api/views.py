from rest_framework.decorators import api_view
from rest_framework.response import Response
from decks.models import Deck, FlashCard

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
