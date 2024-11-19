from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Exists, OuterRef
from decks.models import Deck, FlashCard, CardContent, Category
from django.contrib.auth.models import User
from .serializers import DeckSerializer, FlashCardSerializer, CategorySerializer


# List all available API routes
@api_view(["GET"])
@permission_classes([AllowAny])
@authentication_classes([])
def get_routes(request):
    
    routes = [
        {"GET": "api/decks"},
        {"GET": "api/decks/<int:pk>"},
        {"POST": "api/decks"},
        {"DELETE": "api/decks/<int:pk>"},
        {"PUT": "api/decks/<int:pk>"},
        {"GET": "api/decks/<int:pk>/cards"},
        {"GET": "api/due_decks"},
        {"GET": "api/due_flashcards/<int:pk>"},
        {"GET": "api/all_flashcards/<int:pk>"},
        {"POST": "api/register"},
        {"GET": "api/profile"},
        {"POST": "api/create_flashcard/<int:pk>"},
        {"POST": "api/create_card_content/<int:pk>"},
        {"PUT": "api/update_flashcard/<int:pk>"},
        {"DELETE": "api/delete_flashcard/<int:pk>"},
        {"PUT": "api/update_card_content/<int:pk>"},
        {"DELETE": "api/delete_card_content/<int:pk>"},
    ]
    return Response(routes)


# /////////////////////////////////////////////////////////////////////////
# ------------------------------- DECKS -----------------------------------
# /////////////////////////////////////////////////////////////////////////


# NOTE: (Creates:POST) a deck.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_deck(request):
    data = request.data
    profile = request.user.profile
    name = data.get("name", "NewDeck")
    language = data.get("language", "english")
    description = data.get("description", "")
    category_ids = data.get("category_ids", [])
    parent_deck_id = data.get("parent_deck")

    try:
        # Fetch parent deck if provided
        parent_deck = profile.decks.get(id=parent_deck_id) if parent_deck_id else None

        # Create the new deck
        deck = Deck.objects.create(
            owner=profile,
            parent_deck=parent_deck,
            name=name,
            language=language,
            description=description,
        )

        # Add categories to the deck
        categories = Category.objects.filter(id__in=category_ids, owner=profile)
        deck.categories.set(categories)
        deck.save()

        return Response(DeckSerializer(deck).data, status=status.HTTP_201_CREATED)  
        # 201: Deck successfully created
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  
        # 400: Bad request (e.g., invalid input)



# NOTE: (GET) All decks:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_decks(request):
    profile = request.user.profile
    decks = profile.decks.all()
    serializer = DeckSerializer(decks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# NOTE: (GET) Due decks:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def due_decks(request):
    profile = request.user.profile
    current_time = timezone.now()

    # Filter decks with due flashcards
    due_flashcards = FlashCard.objects.filter(deck=OuterRef("pk"), next_review__lte=current_time)
    due_decks = profile.decks.filter(Exists(due_flashcards)).distinct()

    serializer = DeckSerializer(due_decks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# NOTE: (GET) or (Update:PUT) or (DELETE) a specific deck
@api_view(["GET", "DELETE" , "PUT"])
@permission_classes([IsAuthenticated])
def manage_deck(request, pk):
    profile = request.user.profile

    if request.method == "DELETE":
        try:
            # Fetch and delete the deck
            deck = Deck.objects.get(id=pk, owner=profile)
            deck.delete()
            return Response({"message": "Deck deleted successfully."}, status=status.HTTP_200_OK)  
            # 200: Deck deleted successfully
        except Deck.DoesNotExist:
            return Response({"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND)  
            # 404: Deck does not exist
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
            # 500: Unexpected server error

    if request.method == "GET":
        try:
            # Fetch the deck and return its details
            deck = profile.decks.get(id=pk)
            serializer = DeckSerializer(deck, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)  
            # 200: Deck retrieved successfully
        except Deck.DoesNotExist:
            return Response({"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND)  
            # 404: Deck does not exist
    
    if request.method == "PUT":
        data = request.data

        try:
            deck = profile.decks.get(id=pk)
            deck.name = data.get("name", deck.name)
            deck.description = data.get("description", deck.description)
            deck.language = data.get("language", deck.language)

            # Update categories if provided
            category_ids = data.get("category_ids", [])
            if category_ids:
                categories = Category.objects.filter(id__in=category_ids, owner=profile)
                deck.categories.set(categories)

            deck.save()
            return Response(DeckSerializer(deck).data, status=status.HTTP_200_OK)  # Deck successfully updated
        except Deck.DoesNotExist:
            return Response({"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND)  # Deck does not exist
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  # General error




# NOTE: (Retrieve:GET) completed and due decks
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
        "due_decks": due_decks,
    }
    return Response(data, status=status.HTTP_200_OK)  
    # 200: Successfully retrieved due and completed deck stats
            


# ///////////////////////////////////////////////////////////////////////////
# ------------------------------- CATEGORY -----------------------------------
# ///////////////////////////////////////////////////////////////////////////


# NOTE: (Create:POST) or (retrieve:GET) categories
@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def manage_categories(request):
    profile = request.user.profile

    if request.method == "POST":
        data = request.data
        category_name = data.get("name")

        # Validate category name
        if not category_name:
            return Response({"error": "Category name is required."}, status=status.HTTP_400_BAD_REQUEST)  
            # 400: Missing category name

        # Check if category already exists
        if Category.objects.filter(owner=profile, name=category_name).exists():
            return Response({"error": "Category already exists."}, status=status.HTTP_400_BAD_REQUEST)  
            # 400: Duplicate category name

        # Create and return the new category
        category = Category.objects.create(owner=profile, name=category_name)
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)  
        # 201: Category successfully created

    if request.method == "GET":
        # Retrieve all categories owned by the user
        categories = profile.categories.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
        # 200: Categories retrieved successfully



# NOTE: (Delete) Category:
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_category(request , pk):
    profile = request.user.profile

    try:
        category = profile.categories.get(id=pk)
        category.delete()
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_200_OK)  # Successfully deleted
    except Category.DoesNotExist:
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)  # Category not found
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  # General error


# /////////////////////////////////////////////////////////////////////////////
# ------------------------------- FLASHCARD -----------------------------------
# /////////////////////////////////////////////////////////////////////////////

# NOTE: (Creates:POST) a new flashcard in a specified deck.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_flashcard(request, pk):
    profile = request.user.profile
    try:
        deck = profile.decks.get(id=pk)
        flashcard = FlashCard.objects.create(deck=deck)
        return Response(FlashCardSerializer(flashcard).data, status=status.HTTP_201_CREATED)
    except Deck.DoesNotExist:
        return Response({"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# NOTE: (GET) All flashcards:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_flashcards(request, pk):
    profile = request.user.profile

    try:
        deck = profile.decks.get(id=pk)
        flashcards = deck.flashcards.all()
        serializer = FlashCardSerializer(flashcards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Deck.DoesNotExist:
        return Response({"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND)


# NOTE: (GET) Due Flashcards:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def due_flashcards(request, pk):
    profile = request.user.profile

    try:
        deck = profile.decks.get(id=pk)
        current_time = timezone.now()
        flashcards = deck.flashcards.filter(next_review__lte=current_time)
        serializer = FlashCardSerializer(flashcards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Deck.DoesNotExist:
        return Response({"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Review AND (DELETE) specific flashcard and update its review schedule.
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@api_view(["POST" , "DELETE"])
@permission_classes([IsAuthenticated])
def review_delete_flashcard(request, pk):
    # Review a specific flashcard and update its review schedule.
    if request.method == "POST":
        data = request.data
        try:
            flashcard = FlashCard.objects.get(id=pk, deck__owner=request.user.profile)
            if "review_rating" in data:
                flashcard.update_schedule(review_rating=data["review_rating"])
                return Response({"message": "Flashcard reviewed successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Missing 'review_rating' in request data."}, status=status.HTTP_400_BAD_REQUEST)
        except FlashCard.DoesNotExist:
            return Response({"error": "Flashcard not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == "DELETE":
        try:
            flashcard = FlashCard.objects.get(id=pk, deck__owner=request.user.profile)
            flashcard.delete()
            return Response({"message": "Flashcard deleted successfully."}, status=status.HTTP_200_OK)
        except FlashCard.DoesNotExist:
            return Response({"error": "Flashcard not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

# ////////////////////////////////////////////////////////////////////////////////
# ------------------------------- CARD CONTENT -----------------------------------
# ////////////////////////////////////////////////////////////////////////////////

# NOTE: (Create:POST) content for a specific flashcard.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_card_content(request, pk):
    data = request.data
    try:
        flashcard = FlashCard.objects.get(id=pk, deck__owner=request.user.profile)
        card_content = CardContent.objects.create(
            flashcard=flashcard,
            side=data["side"],
            content_type=data["content_type"],
            text=data.get("text", ""),
            image=data.get("image", None),  # Image is optional
        )
        return Response({"message": "Card content created successfully."}, status=status.HTTP_201_CREATED)
    except FlashCard.DoesNotExist:
        return Response({"error": "Flashcard not found."}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response({"error": "Invalid or missing data."}, status=status.HTTP_400_BAD_REQUEST)



# NOTE: (DELETE) the content of a specific flashcard.
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_card_content(request, pk):
    try:
        # Retrieve the card content by its ID
        card_content = CardContent.objects.get(id=pk, flashcard__deck__owner=request.user.profile)
        card_content.delete()
        return Response({"message": "Card content deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    except CardContent.DoesNotExist:
        return Response({"error": "Card content not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



# ///////////////////////////////////////////////////////////////////////////
# ------------------------------- PROFILE -----------------------------------
# ///////////////////////////////////////////////////////////////////////////

# (Register:POST) a new user
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def register_user(request):
    data = request.data

    # Check for duplicate username or email
    if User.objects.filter(username=data.get("username")).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)  
        # 400: Username already exists
    if User.objects.filter(email=data.get("email")).exists():
        return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)  
        # 400: Email already exists

    try:
        # Create the user
        User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)  
        # 201: User successfully registered
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        # 500: Unexpected server error



# NOTE:(Retrieve:GET) user profile details
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    profile = request.user.profile
    user_data = {
        "username": profile.username,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "email": profile.email,
        "profile_img": request.build_absolute_uri(profile.profile_img.url),
    }
    return Response(user_data, status=status.HTTP_200_OK)  
    # 200: Profile retrieved successfully
