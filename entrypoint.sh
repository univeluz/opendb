#!/bin/sh
set -e

echo "Ma'lumotlar bazasi tayyor bo'lishini kutyapmiz..."
python manage.py wait_for_db

echo "Migratsiyalar bajarilmoqda..."
python manage.py migrate --noinput

echo "Fixture'lar yuklanmoqda (barcha 10 ta, ~3200 yozuv)..."
python manage.py loaddata \
    viloyatlar.json tumanlar.json aholi_punktlari.json banklar.json \
    universitetlar.json valyutalar.json valyuta_kurslari.json \
    bayramlar.json bayram_sanalari.json telefon_kodlari.json

echo "Superuser tekshirilmoqda..."
python manage.py create_default_superuser

echo "Statik fayllar yig'ilmoqda (admin/jazzmin uchun)..."
python manage.py collectstatic --noinput

echo "Gunicorn ishga tushmoqda..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
