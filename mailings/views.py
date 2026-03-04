from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils import timezone
from django.core.mail import send_mail

from attempts.models import MailingAttempt
from mailings.forms import MailingForm
from mailings.models import Mailing


class MailingListView(ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailings/mailing_detail.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:list")


class SendMailingView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        now = timezone.now()

        if now < mailing.start_time:
            messages.error(request, "Рассылка ещё не началась")
            return redirect("mailings:detail", pk=pk)

        if now > mailing.end_time:
            messages.error(request, "Рассылка уже завершена")
            return redirect("mailings:detail", pk=pk)

        success_count = 0
        error_count = 0

        for client in mailing.clients.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email="noreply@example.com",
                    recipient_list=[client.email],
                    fail_silently=False,
                )

                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=MailingAttempt.SUCCESS,
                    server_response="Отправлено успешно",
                )
                success_count += 1

            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing, status=MailingAttempt.FAULT, server_response=str(e)
                )
                error_count += 1

        messages.success(
            request,
            f"Отправлено {success_count} писем успешно, {error_count} с ошибкой",
        )
        return redirect("mailings:detail", pk=pk)
