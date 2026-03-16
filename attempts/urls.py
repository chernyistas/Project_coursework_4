from django.urls import path

from attempts.views import MailingAttemptDetailView, MailingAttemptListView

app_name = "attempts"

urlpatterns = [
    path("", MailingAttemptListView.as_view(), name="list"),
    path("detail/<int:pk>/", MailingAttemptDetailView.as_view(), name="detail"),
]
