from django.urls import path

from mailings.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    SendMailingView

app_name = "mailings"

urlpatterns = [
    path("", MailingListView.as_view(), name="list"),
    path("detail/<int:pk>/", MailingDetailView.as_view(), name="detail"),
    path("create/", MailingCreateView.as_view(), name="create"),
    path("update/<int:pk>/", MailingUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", MailingDeleteView.as_view(), name="delete"),
    path("send/<int:pk>/", SendMailingView.as_view(), name="send"),
]