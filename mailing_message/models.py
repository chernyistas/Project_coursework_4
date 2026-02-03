from django.db import models

class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to="message_attachment/%Y/%m/%d",
          blank=True,
          null=True,
          verbose_name="Вложение")

    def __str__(self):
        return self.subject[:50]

    class Meta:
        verbose_name = "письмо"
        verbose_name_plural = "письма"
        ordering = ["-created_at"]

