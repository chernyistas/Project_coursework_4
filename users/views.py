from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")


class ProfileView(DetailView):
    model = User
    template_name = "users/profile_detail.html"
    context_object_name = "user"


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile_form.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """Возврат текущего пользователя"""
        return self.request.user
