from django.core.cache import cache
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
        if (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            cache_key = "all_messages"
            messages = cache.get(cache_key)
            if messages is None:
                messages = list(Message.objects.all())
                cache.set(cache_key, messages, 300)
            return messages

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
        cache.delete("all_messages")
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

    def form_valid(self, form):
        cache.delete("all_messages")
        return super().form_valid(form)


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

    def delete(self, request, *args, **kwargs):
        cache.delete("all_messages")
        return super().delete(request, *args, **kwargs)
