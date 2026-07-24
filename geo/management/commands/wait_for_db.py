"""
docker-compose'da Django konteyneri Postgres konteyneridan TEZROQ ishga
tushishi mumkin -- shu sabab birinchi migratsiyadan oldin DB haqiqatan
ham so'rovlarni qabul qilishini kutish kerak.
"""
import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Ma'lumotlar bazasi ulanishga tayyor bo'lguncha kutadi"

    def handle(self, *args, **options):
        self.stdout.write("Ma'lumotlar bazasi ulanishi tekshirilmoqda...")
        db_up = False
        attempts = 0
        while not db_up and attempts < 30:
            try:
                connections["default"].cursor()
                db_up = True
            except OperationalError:
                attempts += 1
                self.stdout.write(f"  DB hali tayyor emas, 1 soniyadan keyin qayta urinamiz ({attempts}/30)...")
                time.sleep(1)

        if not db_up:
            self.stderr.write(self.style.ERROR("30 soniyadan keyin ham DB ulanishi topilmadi!"))
            raise SystemExit(1)

        self.stdout.write(self.style.SUCCESS("Ma'lumotlar bazasi tayyor."))
