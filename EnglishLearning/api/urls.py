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
    path("decks/", views.getDecks),
    path("decks/<str:pk>/", views.getDeck),
    path("decks/<str:pk>/cards/", views.getCards),
    path("user/create/", views.createUser),
]
