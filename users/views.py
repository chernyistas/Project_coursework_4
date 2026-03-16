from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, TemplateView,
                                  UpdateView)

from attempts.models import MailingAttempt
from mailings.models import Mailing
from users.forms import UserProfileForm, UserRegisterForm
from users.models import User


class UserStatsView(LoginRequiredMixin, TemplateView):
    template_name = "users/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        mailings = Mailing.objects.filter(owner=user)

        total_mailings = mailings.count()

        attempts = MailingAttempt.objects.filter(mailing__owner=user)
        successful = attempts.filter(status=MailingAttempt.SUCCESS).count()
        failed = attempts.filter(status=MailingAttempt.FAULT).count()
        total_attempts = attempts.count()

        mailing_stats = []
        for mailing in mailings:
            mailing_attempts = attempts.filter(mailing=mailing)
            mailing_stats.append(
                {
                    "mailing": mailing,
                    "total": mailing_attempts.count(),
                    "successful": mailing_attempts.filter(
                        status=MailingAttempt.SUCCESS
                    ).count(),
                    "failed": mailing_attempts.filter(
                        status=MailingAttempt.FAULT
                    ).count(),
                }
            )

        context.update(
            {
                "total_mailings": total_mailings,
                "total_attempts": total_attempts,
                "successful": successful,
                "failed": failed,
                "success_rate": (
                    (successful / total_attempts * 100) if total_attempts > 0 else 0
                ),
                "mailing_stats": mailing_stats,
            }
        )
        return context


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")


class ProfileView(DetailView):
    model = User
    template_name = "users/profile_detail.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        """Возвращает текущего пользователя"""
        return self.request.user


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile_form.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """Возврат текущего пользователя"""
        return self.request.user
