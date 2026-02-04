from django.contrib import admin

from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "short_comment",)
    list_display_links = ("full_name", "email")
    search_fields = ("full_name", "email",)
    ordering = ('email',)
    list_filter = ()
    list_per_page = 20

    def short_comment(self, obj):
        """Отображаем только первые 50 символов комментария"""
        if obj.comment:
            return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
        return "-"

    short_comment.short_description = "Комментарий"