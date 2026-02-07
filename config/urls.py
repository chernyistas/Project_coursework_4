from django.contrib import admin
from django.urls import path, include

from main.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="home"),
    path("clients/", include("clients.urls")),
    path("message/", include("mailing_message.urls")),
    path("mailings/", include("mailings.urls")),
]
