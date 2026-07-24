"""
docker-compose birinchi marta ko'tarilganda admin panelga kirish uchun
superuser avtomatik yaratiladi (.env'dagi DJANGO_SUPERUSER_* qiymatlaridan).
Idempotent -- superuser allaqachon mavjud bo'lsa, hech narsa qilmaydi
(shu sabab konteyner qayta ishga tushirilganda xato bermaydi).
"""
from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "DJANGO_SUPERUSER_* environment o'zgaruvchilaridan superuser yaratadi (mavjud bo'lmasa)"

    def handle(self, *args, **options):
        User = get_user_model()
        username = config("DJANGO_SUPERUSER_USERNAME", default="admin")
        email = config("DJANGO_SUPERUSER_EMAIL", default="admin@opendb.uz")
        password = config("DJANGO_SUPERUSER_PASSWORD", default="")

        if not password:
            self.stdout.write(self.style.WARNING(
                "DJANGO_SUPERUSER_PASSWORD .env'da berilmagan, superuser yaratish o'tkazib yuborildi."
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superuser '{username}' allaqachon mavjud, o'tkazib yuborildi.")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' yaratildi."))
