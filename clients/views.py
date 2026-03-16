from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import Client


class ClientListView(ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"

    def get_queryset(self, queryset=None):
        if (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            cache_key = "all_clients"
            clients = cache.get(cache_key)
            if clients is None:
                clients = list(Client.objects.all())
                cache.set(cache_key, clients, 300)
            return clients

        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(DetailView):
    model = Client
    template_name = "clients/client_detail.html"
    context_object_name = "client"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_superuser:
            return obj
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return obj
        if obj.owner != self.request.user:
            raise PermissionDenied("Это не ваш клиент!")
        return obj


class ClientCreateView(CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        cache.delete("all_clients")
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_superuser:
            return obj
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return obj
        if obj.owner != self.request.user:
            raise PermissionDenied("Это не ваш клиент!")
        return obj

    def form_valid(self, form):
        cache.delete("all_clients")
        return super().form_valid(form)


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_delete_confirm.html"
    success_url = reverse_lazy("clients:list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_superuser:
            return obj
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return obj
        if obj.owner != self.request.user:
            raise PermissionDenied("Это не ваш клиент!")
        return obj

    def delete(self, request, *args, **kwargs):
        cache.delete("all_clients")
        return super().delete(request, *args, **kwargs)
