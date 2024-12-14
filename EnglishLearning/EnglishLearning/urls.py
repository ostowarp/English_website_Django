from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# for get token:
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # get token URL:
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("admin/", admin.site.urls),
    path("api/decks/", include("decks.urls")),
    path("api/users/", include("users.urls")),

    
    path("api/", include("api.urls")),
]

# برای اینکه مدیا های استاتیک خوانده شود:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
