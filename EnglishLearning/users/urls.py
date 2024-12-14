from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ----------------------------------------------------------------------
    # -------------------------- USER PROFILE -----------------------------
    # ----------------------------------------------------------------------
    path("register/", views.register_user, name="register_user"),  # Register a new user
    path("profile/", views.get_profile, name="get_profile"),  # Retrieve user profile details
    path("profile/data/", views.get_profile_data, name="get_profile_data"),  # Get user profile data
    path("profile/update/", views.update_profile, name="update_profile"),  # Update user profile details
    path("profile/delete/", views.delete_profile, name="delete_profile"),  # Delete user profile
    path("profile/decks/count/", views.decks_count, name="decks_count"),  # Get user decks count

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)