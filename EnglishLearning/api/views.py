from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from decks.models import Deck, FlashCard, CardContent, ReviewHistory
from django.contrib.auth.models import User

from django.utils import timezone


from .serializers import DeckSerializer, FlashCardSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET": "api/decks"},
        {"GET": "api/decks/pk"},
        {"GET": "api/decks/pk/cards"},
    ]
    
    return Response(routes)


# create user:
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


# Create Deck:
@api_view(["POST", "PUT"])
@permission_classes([IsAuthenticated])
def createDeck(request):
    data = request.data
    profile = request.user.profile

    try:
        parent_deck = profile.decks.get(id=data["parent_deck"])
    except:
        parent_deck = None

    deck = Deck.objects.create(
        owner=profile,
        name=data["name"],
        parent_deck=parent_deck,
        deck_image=data["deck_image"],
    )

    serializer = DeckSerializer(deck)
    return Response(serializer.data)


# Create FlashCard in deck:
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createFlashCard(request, pk):
    profile = request.user.profile
    deck = profile.decks.get(id=pk)
    flashCard = FlashCard.objects.create(
        deck=deck,
    )
    return Response(flashCard.id)


# crerate card content:
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createCardContent(request, pk):
    data = request.data
    profile = request.user.profile
    flashCard = FlashCard.objects.get(id=pk)
    cardContent = CardContent.objects.create(
        flashcard=flashCard,
        side=data["side"],
        content_type=data["content_type"],
        text=data["text"],
        image=data["image"],
    )


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
def due_flashcards(request, pk):
    profile = request.user.profile
    deck = profile.decks.get(id=pk)
    current_time = timezone.now()
    flashcards = deck.flashcards.filter(next_review__lte=current_time)
    serializer = FlashCardSerializer(flashcards, many=True)
    return Response(serializer.data)

# get All cards of deck:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_flashcards(request , pk):
    profile = request.user.profile
    deck = profile.decks.get(id = pk)
    flashcards = deck.flashcards.all()
    serializer = FlashCardSerializer(flashcards , many=True)
    return Response(serializer.data)
