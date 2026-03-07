from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from clients.models import Client
from mailings.models import Mailing
from mailing_message.models import Message
from users.models import User


class Command(BaseCommand):
    help = "Создание групп с правами"

    def handle(self, *args, **kwargs):
        if Group.objects.filter(name="Менеджеры").exists():
            self.stdout.write(self.style.WARNING("Такая группа уже существует"))
            return

        group = Group.objects.create(name="Менеджеры")

        user_content_type = ContentType.objects.get_for_model(User)
        view_user_permission = Permission.objects.get(
            content_type=user_content_type, codename="view_user"
        )
        group.permissions.add(view_user_permission)

        client_content_type = ContentType.objects.get_for_model(Client)
        view_client_permission = Permission.objects.get(
            content_type=client_content_type, codename="view_client"
        )
        group.permissions.add(view_client_permission)

        message_content_type = ContentType.objects.get_for_model(Message)
        view_message_permission = Permission.objects.get(
            content_type=message_content_type, codename="view_message"
        )
        group.permissions.add(view_message_permission)

        mailing_content_type = ContentType.objects.get_for_model(Mailing)
        view_mailing_permission = Permission.objects.get(
            content_type=mailing_content_type, codename="view_mailing"
        )
        group.permissions.add(view_mailing_permission)

        change_user_permission = Permission.objects.get(
            content_type=user_content_type, codename="change_user"
        )
        group.permissions.add(change_user_permission)

        change_mailing_permission = Permission.objects.get(
            content_type=mailing_content_type, codename="change_mailing"
        )
        group.permissions.add(change_mailing_permission)

        self.stdout.write(
            self.style.SUCCESS("Группа 'Менеджеры' успешно создана с правами!")
        )

