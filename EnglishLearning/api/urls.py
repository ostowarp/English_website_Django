from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes),
    path("decks/", views.getDecks),
    path("decks/<str:pk>/", views.getDeck),
    path("cards/<str:pk>/", views.getCards),
]
