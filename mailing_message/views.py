from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Message

class MessageListView(ListView):
    model = Message
    template_name = "mailing_message/message_list.html"
    context_object_name = "messages"

class MessageDetailView(DetailView):
    model = Message
    template_name = "mailing_message/message_detail.html"
    context_object_name = "message"

class MessageCreateView(CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing_message/message_form.html"
    success_url = reverse_lazy("mailing_message:list")

class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing_message/message_form.html"
    success_url = reverse_lazy("mailing_message:list")

class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailing_message/message_confirm_delete.html"
    success_url = reverse_lazy("mailing_message:list")