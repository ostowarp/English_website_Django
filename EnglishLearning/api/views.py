from rest_framework.decorators import api_view, permission_classes , authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser , AllowAny
from rest_framework.response import Response
from decks.models import Deck, FlashCard, CardContent, ReviewHistory , Category
from django.contrib.auth.models import User

from rest_framework import status
from django.utils import timezone

# for due decks:
from django.db.models import Exists, OuterRef


from .serializers import DeckSerializer, FlashCardSerializer , CategorySerializer





@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET": "api/decks"},
        {"GET": "api/decks/pk"},
        {"GET": "api/decks/pk/cards"},
    ]
    
    return Response(routes)


# Create Deck:
@api_view(["POST", "PUT"])
@permission_classes([IsAuthenticated])
def createDeck(request):
    data = request.data
    profile = request.user.profile
    name = data.get("name" , "NewDeck")
    language = data.get("language" , "english")
    description = data.get("description" , "")
    category_ids = data.get("category_ids" , [])


    try:
        parent_deck = profile.decks.get(id=data["parent_deck"])
    except:
        parent_deck = None

    try:
        deck = Deck.objects.create(
            owner=profile,
            parent_deck=parent_deck,
            name=name,
            language=language,
            description=description,
        )

        # Add categories to the deck:
        categories = Category.objects.filter(id__in=category_ids, owner=profile)
        deck.categories.set(categories)
        deck.save()

        return Response(DeckSerializer(deck).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




# (DELETE) Deck:
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_deck(request , pk):
    profile = request.user.profile
    try:
        deck = Deck.objects.get(id=pk, owner=profile)
        deck.delete()
        return Response({"message": "Deck deleted successfully."}, status=200)
    except Deck.DoesNotExist:
        return Response({"error": "Deck not found."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# Add AND GET Category:
@api_view(["POST" , "GET"])
@permission_classes([IsAuthenticated])
def create_category(request):
    profile = request.user.profile
    if request.method == "POST":
        data = request.data
        category_name = data['name']

        if Category.objects.filter(owner=profile , name = category_name).exists():
            return Response({"error": "Category already exists"} , status=status.HTTP_400_BAD_REQUEST0)
        
        category = Category.objects.create(owner= profile , name = category_name)
        
        serializer = CategorySerializer(category)
        return Response(serializer.data , status=status.HTTP_201_CREATED)
    
    if request.method == "GET":
        categories = profile.categories.all()
        serializer = CategorySerializer(categories , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)


# completed Decks:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def decks_completed(request):
    profile = request.user.profile
    decks = profile.decks.all()
    current_time = timezone.now()
    
    due_flashcards = FlashCard.objects.filter(deck=OuterRef('pk'), next_review__lte=current_time)
    due_decks = decks.filter(Exists(due_flashcards)).distinct().count()

    completed_flashcards = FlashCard.objects.filter(deck=OuterRef('pk'), next_review__gte=current_time)
    completed_decks = decks.filter(Exists(completed_flashcards)).distinct().count()


    data = {
        "completed_decks": completed_decks,
        "due_decks": due_decks
    }
    return Response(data)

# view chart:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def chart_data(request):
    
    return Response()


# register user:
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def registerUser(request):
    data = request.data
    if User.objects.filter(username=data["username"]).exists():
        return Response({"error": "user is exists"}, status=400)
    elif User.objects.filter(email=data["email"]).exists():
        return Response({"error": "email is exists"}, status=400)
    else:
        user = User.objects.create_user(
            first_name=data["first_name"] , last_name=data["last_name"] ,username=data["username"], email=data["email"], password=data["password"]
        )
    return Response({"complete": "user is register"}, status=201)



# Get User Profile image and name:
@api_view(["Get"])
@permission_classes([IsAuthenticated])
def getNameProfile(request):
    profile = request.user.profile
    print(profile.profile_img)
    user = {
        "username":profile.username,
        "first_name":profile.first_name,
        "last_name":profile.last_name,
        "email":profile.email,
        "profile_img":request.build_absolute_uri(profile.profile_img.url)
        
    }
    return Response(user)





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
    return Response()

# Get Due Decks:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def due_decks(request):
    profile = request.user.profile
    decks = profile.decks.all()
    current_time = timezone.now()
    due_flashcards = FlashCard.objects.filter(deck=OuterRef('pk'), next_review__lte=current_time)
    due_decks = decks.filter(Exists(due_flashcards)).distinct()
    serializer = DeckSerializer(due_decks , many = True)
    return Response(serializer.data)

# get Decks:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_decks(request):
    profile = request.user.profile
    decks = profile.decks.all()
    serializer = DeckSerializer(decks, many=True)
    return Response(serializer.data)

# NOTE:
# get single Deck:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def single_deck(request, pk):
    profile = request.user.profile
    deck = profile.decks.get(id=pk)
    serializer = DeckSerializer(deck, many=False)
    current_time = timezone.now()
    print(deck.flashcards.filter(next_review__gte=current_time).count())
    return Response(serializer.data)


# get Due Cards of deck:
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


# Review Flashcard:
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def review_flashcard(request , pk):
    data = request.data
    flashcard = FlashCard.objects.get(id = pk)
    flashcard.update_schedule(review_rating=data['review_rating'])
    return Response()