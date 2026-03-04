from django.db import models
from django.utils import timezone
from clients.models import Client
from mailing_message.models import Message


class Mailing(models.Model):
    CREATED = "created"
    STARTED = "started"
    COMPLETED = "completed"

    CHOICES_STATUS = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (COMPLETED, "Завершена")
    ]
    start_time = models.DateTimeField(verbose_name="Время начала рассылки")
    end_time = models.DateTimeField(verbose_name="Время окончания рассылки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=15, choices=CHOICES_STATUS, default=CREATED, verbose_name="Статус")
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="mailings", verbose_name="Сообщение")

    def __str__(self):
        return f"Рассылка #{self.id}: {self.message.subject[:30]}..."

    def update_status(self):
        now = timezone.now()

        if now < self.start_time:
            new_status = self.CREATED
        elif self.start_time <= now <= self.end_time:
            new_status = self.STARTED
        else:
            new_status = self.COMPLETED

        if self.status != new_status:
            self.status = new_status
            self.save()

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["-created_at"]