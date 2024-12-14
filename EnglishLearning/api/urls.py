from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    # List all API routes
    path("routes/", views.get_routes, name="get_routes"),

    


]