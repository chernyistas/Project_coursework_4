from django.views.generic import ListView, DetailView

from attempts.models import MailingAttempt


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "attempts/mailing_attempt_list.html"
    context_object_name = "attempts"


class MailingAttemptDetailView(DetailView):
    model = MailingAttempt
    template_name = "attempts/mailing_attempt_detail.html"
    context_object_name = "attempt"
