from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("decks/", views.decks, name="decks"),
    path("deckform/", views.createDeck, name="deckform"),
    path("deck/<str:pk>/", views.deck, name="singledeck"),
    path("updateform/<str:pk>", views.updateDeck, name="updatedeck"),
]
