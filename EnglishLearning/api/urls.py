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
    # List all API routes
    path("routes/", views.get_routes, name="get_routes"),

    # get token URL:
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    
    # ----------------------------------------------------------------------
    # -------------------------- USER PROFILE -----------------------------
    # ----------------------------------------------------------------------
    path("register/", views.register_user, name="register_user"),  # Register a new user
    path("profile/", views.get_profile, name="get_profile"),  # Retrieve user profile details

    
    # ----------------------------------------------------------------------
    # -------------------------- DECKS -------------------------------------
    # ----------------------------------------------------------------------
    path('decks/create/', views.create_deck, name='create_deck'), # create(POST) a new deck
    path('decks/all/', views.all_decks, name='all_decks'), # (Get) All Deck
    path('decks/', views.due_decks, name='due_decks'), # (Get) Due Deck
    path('decks/<str:pk>/', views.manage_deck, name='manage_deck'), # (Get) , (update) , or (delete) a specific deck
    path('completed/decks/', views.decks_completed, name='decks_completed'), # Retrieve(Get) completed and due decks


    # ----------------------------------------------------------------------
    # ------------------------ FLASHCARDS ----------------------------------
    # ----------------------------------------------------------------------
    path('decks/<str:pk>/cards/all/', views.all_flashcards, name='all_flashcards'), # (get) all flashcards of specific deck
    path('decks/<str:pk>/cards/', views.due_flashcards, name='due_flashcards'), # (get) due flashcards of specific deck
    path('decks/<str:pk>/flashcard/', views.create_flashcard, name='create_flashcard'), # create(post) flashcard in specific deck
    path('flashcards/<str:pk>/', views.review_delete_update_flashcard, name='delete_flashcard'), # review and delete specific flashcard
    path('decks/images/<str:pk>/' , views.upload_deck_image , name="uload_image"),

    # ----------------------------------------------------------------------
    # -------------------------- CATEGORIES --------------------------------
    # ----------------------------------------------------------------------
    path('categories/', views.manage_categories, name='manage_categories'), # get all categories or add new category
    path('categories/<str:pk>/', views.delete_category, name='delete_category'), # delete a specific category

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)