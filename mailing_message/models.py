from django.db import models

from users.models import User


class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(
        upload_to="message_attachment/", blank=True, null=True, verbose_name="Вложение"
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="messages", null=True, blank=True
    )

    def __str__(self):
        return self.subject[:50]

    class Meta:
        verbose_name = "письмо"
        verbose_name_plural = "письма"
        ordering = ["-created_at"]
