from django.contrib import admin

from .models import MailingAttempt


@admin.register(MailingAttempt)
class MailAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt_time", "status", "mailing", "short_response")
    list_filter = ("status", "attempt_time")
    search_fields = ("server_response", "mailing__id")
    readonly_fields = ("attempt_time",)
    ordering = ("-attempt_time",)

    def short_response(self, obj):
        """Отображаем только первые 50 символов ответа сервера"""
        if obj.server_response:
            return (
                obj.server_response[:50] + "..."
                if len(obj.server_response) > 50
                else obj.server_response
            )
        return "-"

    short_response.short_description = "Ответ сервера"
