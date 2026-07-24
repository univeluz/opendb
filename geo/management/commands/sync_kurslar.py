"""
CBU rasmiy JSON API'sidan valyuta kurslarini yangilaydi.
Ishlatish: python manage.py sync_kurslar
Rejalashtirish (production'da): cron bilan har kuni, masalan:
    0 12 * * * cd /app && python manage.py sync_kurslar
(Celery ulanganda buni Celery beat periodic task qilish mumkin.)
"""
from datetime import datetime

import requests
from django.core.management.base import BaseCommand

from geo.models import Valyuta, ValyutaKursi

CBU_API_URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"


class Command(BaseCommand):
    help = "CBU API'dan valyuta va kunlik kurslarni yangilaydi"

    def handle(self, *args, **options):
        self.stdout.write("CBU API'ga so'rov yuborilmoqda...")
        response = requests.get(CBU_API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        yangilangan, yaratilgan = 0, 0
        for item in data:
            valyuta, _ = Valyuta.objects.update_or_create(
                cbu_id=item["id"],
                defaults=dict(
                    iso_numeric_code=item["Code"],
                    code=item["Ccy"],
                    name_uz=item["CcyNm_UZ"],
                    name_uz_cyrl=item["CcyNm_UZC"],
                    name_ru=item["CcyNm_RU"],
                    name_en=item["CcyNm_EN"],
                    nominal=int(item["Nominal"]),
                ),
            )
            _, created = ValyutaKursi.objects.update_or_create(
                valyuta=valyuta,
                sana=datetime.strptime(item["Date"], "%d.%m.%Y").date(),
                defaults=dict(rate=item["Rate"], diff=item["Diff"]),
            )
            yaratilgan += int(created)
            yangilangan += int(not created)

        self.stdout.write(self.style.SUCCESS(
            f"Tayyor: {len(data)} valyuta qayta ishlandi "
            f"({yaratilgan} yangi kurs, {yangilangan} yangilangan)."
        ))
