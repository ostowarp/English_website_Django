from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("decks/", views.decks, name="decks"),
    path("deckfrom" , views.createDeck , name="deckform"),
    path("deck/<str:pk>/", views.deck, name="singledeck"),
]
