from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from main.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("clients/", include("clients.urls")),
    path("message/", include("mailing_message.urls")),
    path("mailings/", include("mailings.urls")),
    path("attempts/", include("attempts.urls")),
    path("users/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
