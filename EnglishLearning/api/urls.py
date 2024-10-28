# for get token:
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from . import views

urlpatterns = [
    # get token URL:
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", views.getRoutes),
    # create deck:
    path("decks/create/",views.createDeck),
    # create flashcard:
    path('decks/<str:pk>/cards/create' , views.createFlashCard),
    path('decks/cards/<str:pk>/content/create' , views.createCardContent),
    path("decks/", views.due_decks),
    path("decks/all", views.all_decks),
    path("decks/<str:pk>/", views.single_deck),
    path("decks/<str:pk>/cards/", views.due_flashcards),
    path("decks/<str:pk>/cards/all", views.all_flashcards),
    path("user/create/", views.createUser),
    path("decks/cards/<str:pk>/review", views.review_flashcard),
]
