from django.core.cache import cache
from django.views.generic import TemplateView

from clients.models import Client
from mailings.models import Mailing


class HomeView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_key_total = "total_mailings"
        cache_key_active = "active_mailings"
        cache_key_clients = "unique_clients"

        total_mailings = cache.get(cache_key_total)
        active_mailings = cache.get(cache_key_active)
        unique_clients = cache.get(cache_key_clients)

        if total_mailings is None:
            total_mailings = Mailing.objects.count()
            cache.set(cache_key_total, total_mailings, 300)

        if active_mailings is None:
            active_mailings = Mailing.objects.filter(status="started").count()
            cache.set(cache_key_active, active_mailings, 300)

        if unique_clients is None:
            unique_clients = Client.objects.count()
            cache.set(cache_key_clients, unique_clients, 300)

        context["total_mailings"] = total_mailings
        context["active_mailings"] = active_mailings
        context["unique_clients"] = unique_clients

        return context
