from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # ----------------------------------------------------------------------
    # -------------------------- CATEGORIES --------------------------------
    # ----------------------------------------------------------------------
    path('categories/', views.manage_categories, name='manage_categories'), # GET: All categories, POST: Create category
    path('categories/delete/<str:pk>/', views.delete_category, name='delete_category'), # DELETE: Specific category

    # ----------------------------------------------------------------------
    # -------------------------- DECKS -------------------------------------
    # ----------------------------------------------------------------------
    path('', views.due_decks, name='due_decks'), # (GET) Due Decks
    path('create/', views.create_deck, name='create_deck'), # (POST) Create a new deck
    path('all/', views.all_decks, name='all_decks'), # (GET) All Decks
    path('<str:pk>/', views.manage_deck, name='manage_deck'), # (GET, PUT, DELETE) Specific Deck
    path('completed/decks/', views.decks_completed, name='decks_completed'), # (GET) Completed and Due Decks

    # ----------------------------------------------------------------------
    # ------------------------ FLASHCARDS ----------------------------------
    # ----------------------------------------------------------------------
    path('<str:pk>/cards/all/', views.all_flashcards, name='all_flashcards'), # (GET) All Flashcards of Deck
    path('<str:pk>/cards/', views.due_flashcards, name='due_flashcards'), # (GET) Due Flashcards of Deck
    path('<str:pk>/flashcard/', views.create_flashcard, name='create_flashcard'), # (POST) Create Flashcard in Deck
    path('flashcards/<str:pk>/', views.review_delete_update_flashcard, name='delete_flashcard'), # (POST, DELETE, PUT) Specific Flashcard
    path('images/<str:pk>/', views.upload_deck_image, name="upload_image"), # (POST) Upload Image for Deck
    path('chartdata/week/', views.chart_data_week, name="chartdata_week"), # (GET) Chart Data for Week
    path('chartdata/month/', views.chart_data_month, name="chartdata_month"), # (GET) Chart Data for Month

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
