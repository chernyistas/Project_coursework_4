from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from attempts.models import MailingAttempt
from mailings.models import Mailing


class Command(BaseCommand):
    help = "Отправляет все активные рассылки"

    def add_arguments(self, parser):
        parser.add_argument(
            "--mailing-id",
            type=int,
            help="ID конкретной рассылки для отправки",
        )

    def handle(self, *args, **options):
        now = timezone.now()

        if options["mailing_id"]:
            mailings = Mailing.objects.filter(
                pk=options["mailing_id"],
                status="started",
                start_time__lte=now,
                end_time__gte=now,
            )
        else:
            mailings = Mailing.objects.filter(
                status="started", start_time__lte=now, end_time__gte=now
            )

        if not mailings.exists():
            self.stdout.write(self.style.WARNING("Нет активных рассылок для отправки"))
            return

        total_sent = 0
        total_errors = 0

        for mailing in mailings:
            self.stdout.write(
                f"Отправка рассылки #{mailing.id}: {mailing.message.subject}"
            )

            mailing_sent = 0
            mailing_errors = 0

            for client in mailing.clients.all():
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email="noreplay@example.com",
                        recipient_list=[client.email],
                        fail_silently=False,
                    )

                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status=MailingAttempt.SUCCESS,
                        server_response="Отправлено через команду",
                    )
                    mailing_sent += 1

                except Exception as e:
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status=MailingAttempt.FAULT,
                        server_response=str(e),
                    )
                    mailing_errors += 1
                    self.stdout.write(
                        self.style.ERROR(f"Ошибка для {client.email}: {e}")
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Рассылка #{mailing.id}: отправлено {mailing_sent}, ошибок {mailing_errors}"
                )
            )
            total_sent += mailing_sent
            total_errors += mailing_errors

        self.stdout.write("=" * 50)
        self.stdout.write(
            self.style.SUCCESS(
                f"ИТОГО: обработано рассылок: {mailings.count()}, "
                f"отправлено писем: {total_sent}, "
                f"ошибок: {total_errors}"
            )
        )
