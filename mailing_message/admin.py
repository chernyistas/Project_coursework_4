from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "short_body", "created_at")
    list_filter = ("created_at",)
    search_fields = ("body", "subject")
    ordering = ("subject",)
    list_display_links = ("subject",)

    def short_body(self, obj: Message) -> str:
        """Отображаем только первые 50 символов письма"""
        if obj.body:
            return obj.body[:50] + "..." if len(obj.body) > 50 else obj.body
        return "-"

    short_body.short_description = "Текст письма"  # type: ignore[attr-defined]
