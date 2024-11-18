from django.conf import settings
from django.conf.urls.static import static


# for get token:
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from . import views

urlpatterns = [
    # Note view all API request:
    # registerUser:
    path("user/create/", views.registerUser),
    
    path("", views.getRoutes),
    # get token URL:
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),


    # create deck:
    path("decks/create/",views.createDeck),
    path("categories/" , views.create_category),
    
    # (DELETE) deck:
    path("decks/<str:pk>/delete/" , views.delete_deck),

    # Decks Completed:
    path("deckcompleted/" ,views.decks_completed ),

    # create flashcard:
    path('decks/<str:pk>/cards/create' , views.createFlashCard),
    path('cards/<str:pk>/content/create' , views.createCardContent),
    path("decks/", views.due_decks),
    path("decks/all", views.all_decks),
    path("decks/<str:pk>/", views.single_deck),
    path("decks/<str:pk>/cards/", views.due_flashcards),
    path("decks/<str:pk>/cards/all", views.all_flashcards),
    path("cards/<str:pk>/review", views.review_flashcard),
    
    
    path("getnameprof/", views.getNameProfile),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)