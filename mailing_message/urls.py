from django.urls import path

from mailing_message.views import (MessageCreateView, MessageDeleteView,
                                   MessageDetailView, MessageListView,
                                   MessageUpdateView)

app_name = "mailing_message"

urlpatterns = [
    path("", MessageListView.as_view(), name="list"),
    path("detail/<int:pk>/", MessageDetailView.as_view(), name="detail"),
    path("create/", MessageCreateView.as_view(), name="create"),
    path("update/<int:pk>/", MessageUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", MessageDeleteView.as_view(), name="delete"),
]
