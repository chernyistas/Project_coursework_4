from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Создание суперпользователя с email admin@sky.pro"

    def handle(self, *args, **kwargs):
        if User.objects.filter(email="admin@sky.pro").exists():
            self.stdout.write(
                self.style.WARNING("Пользователь admin@sky.pro уже существует")
            )
            return

        user = User.objects.create(email="admin@sky.pro")
        user.set_password("123qwe")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(
            self.style.SUCCESS(f"Суперпользователь создан: {user.email}!")
        )
