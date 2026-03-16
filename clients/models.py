from django.db import models

from users.models import User


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Почта")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="clients",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ["email"]
