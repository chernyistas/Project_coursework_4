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


class ClientDetailView(DetailView):
    model = Client
    template_name = "clients/client_detail.html"
    context_object_name = "client"


class ClientCreateView(CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:list")


class ClientUpdateView(UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_delete_confirm.html"
    success_url = reverse_lazy("clients:list")
