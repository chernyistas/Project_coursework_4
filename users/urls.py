from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import ProfileView, RegisterView, ProfileUpdateView

app_name = "users"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
