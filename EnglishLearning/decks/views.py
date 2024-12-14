from django.utils import timezone
from django.db.models import Count, OuterRef
from django.db.models.functions import TruncDate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Exists, OuterRef

from decks.models import Deck, FlashCard, Category, DeckImage, ReviewHistory
from decks.serializers import DeckSerializer, FlashCardSerializer, CategorySerializer




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
        # if deck is existing then return error:
        if Deck.objects.filter(owner=profile, name=name).exists():
            return Response({"error": "Deck already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Add categories to the deck
        categories = Category.objects.filter(id__in=category_ids, owner=profile)
        deck.categories.set(categories)
        deck.save()

        return Response(DeckSerializer(deck).data, status=status.HTTP_201_CREATED)
    except Deck.DoesNotExist:
        return Response({"error": "Parent deck not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # 400: Bad request (e.g., invalid input)


# NOTE: (GET) All decks:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_decks(request):
    """
    Retrieve all decks for the authenticated user with optional filtering.
    
    Query Parameters:
        - categories (list): Filter decks by category names.
        - language (str): Filter decks by language.
        - minCardNumber (int): Minimum number of flashcards in a deck.
        - maxCardNumber (int): Maximum number of flashcards in a deck.
    
    Returns:
        JSON response containing the list of filtered decks.
    """
    profile = request.user.profile
    decks = profile.decks.all()

    # Extract filter parameters
    categories = request.query_params.getlist("categories[]", [])
    language = request.query_params.get("language", None)
    min_card_number = request.query_params.get("minCardNumber", None)
    max_card_number = request.query_params.get("maxCardNumber", None)

    # Apply category filter if provided
    if categories:
        decks = decks.filter(categories__name__in=categories)

    # Apply language filter if provided
    if language:
        decks = decks.filter(language__iexact=language)

    # Apply flashcard count filters if provided
    if min_card_number or max_card_number:
        decks = decks.annotate(card_count=Count('flashcards'))
        if min_card_number:
            try:
                min_card_number = int(min_card_number)
                decks = decks.filter(card_count__gte=min_card_number)
            except ValueError:
                return Response(
                    {"error": "minCardNumber must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if max_card_number:
            try:
                max_card_number = int(max_card_number)
                decks = decks.filter(card_count__lte=max_card_number)
            except ValueError:
                return Response(
                    {"error": "maxCardNumber must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )

    # Ensure distinct results
    decks = decks.distinct()
    print("deeeeeeeeckkkkkk:")
    print(decks)

    # Serialize the queryset
    serializer = DeckSerializer(decks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# NOTE: (GET) Due decks:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def due_decks(request):
    profile = request.user.profile
    current_time = timezone.now()

    # Filter decks with due flashcards
    due_flashcards = FlashCard.objects.filter(
        deck=OuterRef("pk"), next_review__lte=current_time
    )
    due_decks = profile.decks.filter(Exists(due_flashcards)).distinct()

    serializer = DeckSerializer(due_decks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# NOTE: (GET) or (Update:PUT) or (DELETE) a specific deck
@api_view(["GET", "DELETE", "PUT"])
@permission_classes([IsAuthenticated])
def manage_deck(request, pk):
    profile = request.user.profile
    # Delete a deck:
    if request.method == "DELETE":
        try:
            # Fetch and delete the deck
            deck = Deck.objects.get(id=pk, owner=profile)
            deck.delete()
            return Response(
                {"message": "Deck deleted successfully."}, status=status.HTTP_200_OK
            )
            # 200: Deck deleted successfully
        except Deck.DoesNotExist:
            return Response(
                {"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND
            )
            # 404: Deck does not exist
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            # 500: Unexpected server error

    # Get a specific deck:
    if request.method == "GET":
        try:
            # Fetch the deck and return its details
            deck = profile.decks.get(id=pk)
            serializer = DeckSerializer(deck, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
            # 200: Deck retrieved successfully
        except Deck.DoesNotExist:
            return Response(
                {"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND
            )
            # 404: Deck does not exist

    # Update a deck:
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
            return Response(
                DeckSerializer(deck).data, status=status.HTTP_200_OK
            )  # Deck successfully updated
        except Deck.DoesNotExist:
            return Response(
                {"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND
            )  # Deck does not exist
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )  # General error


# NOTE: (Retrieve:GET) completed and due decks
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def decks_completed(request):
    profile = request.user.profile
    decks = profile.decks.all()
    current_time = timezone.now()

    due_flashcards = FlashCard.objects.filter(
        deck=OuterRef("pk"), next_review__lte=current_time
    )
    due_decks = decks.filter(Exists(due_flashcards)).distinct().count()

    completed_decks = decks.count() - due_decks
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
            return Response(
                {"error": "Category name is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            # 400: Missing category name

        # Check if category already exists
        if Category.objects.filter(owner=profile, name=category_name).exists():
            return Response(
                {"error": "Category already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            # 400: Duplicate category name

        # Create and return the new category
        category = Category.objects.create(owner=profile, name=category_name)
        return Response(
            CategorySerializer(category).data, status=status.HTTP_201_CREATED
        )
        # 201: Category successfully created

    if request.method == "GET":
        # Retrieve all categories owned by the user
        categories = Category.objects.filter(owner=profile)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # 200: Categories retrieved successfully



# NOTE: (Delete) Category:
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_category(request, pk):
    profile = request.user.profile

    try:
        category = profile.categories.get(id=pk)
        category.delete()
        return Response(
            {"message": "Category deleted successfully."}, status=status.HTTP_200_OK
        )  # Successfully deleted
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND
        )  # Category not found
    except Exception as e:
        return Response(
            {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )  # General error


# /////////////////////////////////////////////////////////////////////////////
# ------------------------------- FLASHCARD -----------------------------------
# /////////////////////////////////////////////////////////////////////////////


# NOTE: (Creates:POST) a new flashcard in a specified deck.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_flashcard(request, pk):

    data = request.data
    front = data.get("front")
    back = data.get("back")
    profile = request.user.profile
    try:
        deck = profile.decks.get(id=pk)
        flashcard = FlashCard.objects.create(deck=deck, front=front, back=back)
        return Response(
            FlashCardSerializer(flashcard).data, status=status.HTTP_201_CREATED
        )
    except Deck.DoesNotExist:
        return Response({"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Upload image for flashcard:
@api_view(["POST"])
@permission_classes([])
def upload_deck_image(request, pk):
    # profile = request.user.profile
    uploaded_file = request.FILES.get("upload")
    deck_id = pk

    if not uploaded_file or not deck_id:
        return Response(
            {"error": "Please provide both an image file and a valid Deck_id."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Fetch the flashcard
        deck = Deck.objects.get(id=pk)
    except Deck.DoesNotExist:
        return Response(
            {"error": "Deck not found or you don't have permission to modify it."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Save the uploaded image
    deck_image = DeckImage.objects.create(
        deck=deck,
        image=uploaded_file,
    )

    # Construct the URL for the uploaded image
    file_url = request.build_absolute_uri(deck_image.image.url)

    return Response(
        {"uploaded": True, "url": file_url},
        status=status.HTTP_201_CREATED,
    )


# NOTE: (GET) All flashcards:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_flashcards(request, pk):
    profile = request.user.profile

    try:
        deck = profile.decks.get(id=pk)
        flashcards = deck.flashcards.all().order_by("next_review")
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
        flashcards = deck.flashcards.filter(next_review__lte=current_time).order_by("next_review")
        serializer = FlashCardSerializer(flashcards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Deck.DoesNotExist:
        return Response({"error": "Deck not found."}, status=status.HTTP_404_NOT_FOUND)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Review AND (DELETE) specific flashcard and update its review schedule.
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@api_view(["POST", "DELETE", "PUT"])
@permission_classes([IsAuthenticated])
def review_delete_update_flashcard(request, pk):
    profile = request.user.profile
    # Review a specific flashcard and update its review schedule.
    if request.method == "POST":
        data = request.data
        try:
            flashcard = FlashCard.objects.get(id=pk, deck__owner=request.user.profile)
            if "review_rating" in data:
                flashcard.update_schedule(review_rating=data["review_rating"])
                return Response(
                    {"message": "Flashcard reviewed successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Missing 'review_rating' in request data."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except FlashCard.DoesNotExist:
            return Response(
                {"error": "Flashcard not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    if request.method == "DELETE":
        try:
            flashcard = FlashCard.objects.get(id=pk, deck__owner=profile)
            flashcard.delete()
            return Response(
                {"message": "Flashcard deleted successfully."},
                status=status.HTTP_200_OK,
            )
        except FlashCard.DoesNotExist:
            return Response(
                {"error": "Flashcard not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    if request.method == "PUT":
        data = request.data
        try:
            flashcard = FlashCard.objects.get(id=pk, deck__owner=profile)
            flashcard.front = data.get("front")
            flashcard.back = data.get("back")
            flashcard.save()
            return Response(
                {"message": "Flashcard Update successfully."}, status=status.HTTP_200_OK
            )
        except FlashCard.DoesNotExist:
            return Response(
                {"error": "Flashcard not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# (get)review at week:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def chart_data_week(request):
    # Get the user's profile from the request
    profile = request.user.profile
    current_time = timezone.now()

    # Calculate the date 7 days ago
    seven_days_ago = current_time - timezone.timedelta(days=7)

    try:
        # Query to get the review stats for the last 7 days
        review_stats = (
            ReviewHistory.objects.filter(
                flashcard__deck__owner=profile, reviewed_at__gte=seven_days_ago
            )
            .annotate(review_date=TruncDate("reviewed_at"))
            .values("review_date")
            .annotate(count=Count("id"))
            .order_by("review_date")
        )

        # Prepare a list of the last 7 days including today
        date_list = [
            seven_days_ago + timezone.timedelta(days=i) for i in range(1, 8)
        ]

        # Map each date to its corresponding day name and count
        days_map = {date.date(): 0 for date in date_list}
        for stat in review_stats:
            days_map[stat["review_date"]] = stat["count"]

        # Create the response data with ordered dates
        response_data = [
            {"day": date.strftime("%a"), "count": days_map[date.date()]}
            for date in date_list
        ]

        # Return the response with the data
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle unexpected errors and return a 500 error with the error message
        return Response({"error": str(e)}, status=500)



# last month:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def chart_data_month(request):
    # Get the user's profile from the request
    profile = request.user.profile
    current_time = timezone.now()

    # Calculate the date 30 days ago
    thirty_days_ago = current_time - timezone.timedelta(days=30)

    try:
        # Query to get the review stats for the last 30 days, grouped by the exact date of the review
        review_stats = (
            ReviewHistory.objects.filter(flashcard__deck__owner=profile, reviewed_at__gte=thirty_days_ago)
            .annotate(review_date=TruncDate("reviewed_at"))  # Truncate the datetime to just the date
            .values("review_date")
            .annotate(count=Count("id"))
            .order_by("review_date")  # Ensure the data is ordered by date
        )
        
        
        # Prepare the dictionary to hold the day and count of reviews (initialized to 0)
        all_days = {day: 0 for day in range(1, 32)}  # Days 1 to 31 initialized to 0

        # Update the dictionary with actual review counts for days that have reviews
        for day in review_stats:
            day_of_month = day["review_date"].day
            all_days[day_of_month] = day["count"]

        # Prepare the list of days (1 to 31)
        ordered_days = list(range(1, 32))

        # Sort the list so that today comes last
        today_day = current_time.day  # Get the current day of the month
        ordered_days = ordered_days[today_day:] + ordered_days[:today_day]  # Place today at the end

        # Prepare the response data with days and their review counts
        response_data = [{"day": day, "count": all_days[day]} for day in ordered_days]

        # If no reviews are found, handle that case
        if not response_data:
            return Response({"message": "No reviews found for the last 30 days."}, status=404)

        # Return the response with the data
        return Response(response_data)

    except Exception as e:
        # Handle unexpected errors and return a 500 error with the error message
        return Response({"error": str(e)}, status=500)
