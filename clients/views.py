from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Client


class ClientListView(ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"

    def get_queryset(self, queryset=None):
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(DetailView):
    model = Client
    template_name = "clients/client_detail.html"
    context_object_name = "client"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
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
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("Это не ваш клиент!")
        return obj


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_delete_confirm.html"
    success_url = reverse_lazy("clients:list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("Это не ваш клиент!")
        return obj
