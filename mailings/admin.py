from django.contrib import admin

from .models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_time",
        "end_time",
        "created_at",
        "status",
        "short_message",
        "clients_count",
    )
    filter_horizontal = ("clients",)
    list_filter = ("created_at", "start_time", "status")
    search_fields = ("message__subject", "message__body")
    ordering = ("-created_at",)
    list_display_links = ("id", "short_message")

    def short_message(self, obj: Mailing) -> str:
        """Краткое описание сообщения"""
        return (
            f"{obj.message.subject[:30]}..."
            if len(obj.message.subject) > 30
            else obj.message.subject
        )

    short_message.short_description = "Сообщение"  # type: ignore[attr-defined]

    def clients_count(self, obj):
        """Количество клиентов в рассылке"""
        return obj.clients.count()

    clients_count.short_description = "Количество клиентов"  # type: ignore[attr-defined]
