from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response



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







# # search decks:
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def search_decks(request):  
#     searchtext = request.data.get("searchtext", "")
#     language = request.data.get("language", "")
#     categories = request.data.get("categories", [])
#     profile = request.user.profile
#     try:    
#         # search by card content or deck name and return decks:
#         decks_name = profile.decks.filter(name__icontains=searchtext)
#         decks_question = profile.decks.filter(flashcards__question__icontains=searchtext)
#         decks = (decks_name | decks_question).distinct()
#         # add some filters:
#         if language:
#             decks = decks.filter(language=language)
#         # if categories:
#         #     decks = decks.filter(categories__in=categories)
#         serializer = DeckSerializer(decks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


