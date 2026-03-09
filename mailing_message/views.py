from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import Message


class MessageListView(ListView):
    model = Message
    template_name = "mailing_message/message_list.html"
    context_object_name = "messages"

    def get_queryset(self, queryset=None):
        if self.request.user.is_superuser:
            return Message.objects.all()
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView):
    model = Message
    template_name = "mailing_message/message_detail.html"
    context_object_name = "message"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_superuser:
            return obj
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return obj
        if obj.owner != self.request.user:
            raise PermissionDenied("Это не ваш клиент")
        return obj


class MessageCreateView(CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing_message/message_form.html"
    success_url = reverse_lazy("mailing_message:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing_message/message_form.html"
    success_url = reverse_lazy("mailing_message:list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_superuser:
            return obj
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return obj
        if obj.owner != self.request.user:
            raise PermissionDenied("Это не ваш клиент")
        return obj


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailing_message/message_confirm_delete.html"
    success_url = reverse_lazy("mailing_message:list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_superuser:
            return obj
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return obj
        if obj.owner != self.request.user:
            raise PermissionDenied("Это не ваш клиент")
        return obj
