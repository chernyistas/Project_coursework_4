from django.db import models

from mailings.models import Mailing


class MailingAttempt(models.Model):
    SUCCESS = "success"
    FAULT = "fault"

    TRYING_CHOICES_STATUS = [
        (SUCCESS, "Успешно"),
        (FAULT, "Не успешно")
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=20, choices=TRYING_CHOICES_STATUS,
                                       default=SUCCESS, verbose_name="Статусы попытки")
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", related_name="attempts")

    def __str__(self):
        return f"Попытка: {self.id}({self.get_status_display()}) для рассылки #{self.mailing.id}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"
        ordering = ["-attempt_time"]