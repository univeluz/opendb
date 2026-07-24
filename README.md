# OpenDB (opendb.uz)

O'zbekiston uchun ochiq ma'lumotlar API'si — MVP.

## Tayyor bo'lgan qism

**11 model, 3228 ta real yozuv**, hammasi ishonchli manbalardan yig'ilgan va
tekshirilgan (batafsili -- [`DATA_SOURCES.md`](./DATA_SOURCES.md)):

| Model | Soni | Manba |
|---|---|---|
| Viloyat | 14 | ISO 3166-2:UZ + SOATO |
| Tuman | 209 | SOATO-asoslangan (community, tekshirilgan) |
| AholiPunkti | 2631 | SOATO-asoslangan (community, tekshirilgan) |
| Bank | 35 | O'zbekiston Markaziy banki (rasmiy) |
| OTM | 136 | oliygoh.uz (faqat davlat OTMlari) |
| Valyuta / ValyutaKursi | 74 + 74 | Markaziy bank rasmiy JSON API |
| Bayram / BayramSanasi | 11 + 17 | Prezident Farmoni PF-257 + Mehnat kodeksi |
| TelefonKodi | 27 | Rasmiy raqamlash tizimi + goldenpages.uz |
| Namoz vaqtlari | — (hisoblanadi) | NOAA formulasi, 2 mavsumda validatsiya qilingan |

## Texnologiyalar

- **Django 6 + DRF** -- API
- **PostgreSQL** -- ma'lumotlar bazasi (docker-compose orqali)
- **django-jazzmin** -- zamonaviy admin panel ko'rinishi
- **django-import-export** -- admin orqali CSV/XLSX/JSON import-eksport
- **drf-spectacular** -- avtomatik Swagger/OpenAPI hujjatlari
- **python-decouple** -- `.env` orqali sozlamalar
- **django-filter** -- API'da `?viloyat=1` kabi filtrlash
- **whitenoise** -- statik fayllar (nginx'siz, admin/jazzmin CSS uchun)
- **Gunicorn** -- production WSGI server
- **Docker + docker-compose** -- bitta buyruq bilan ishga tushirish

**Hozircha YO'Q (keyingi bosqichlar uchun qoldirilgan, rasmga qarang):**
Redis, Celery (valyuta kursini avtomatik yangilash uchun kerak bo'ladi --
`models.py` ichida tayyor komanda namunasi bor), JWT (hozircha himoyalanishi
kerak bo'lgan resurs yo'q -- API to'liq ochiq/o'qish-uchun), Nginx (whitenoise
hozircha yetarli), GitHub Actions CI/CD.

## Ishga tushirish

```bash
git clone <repo-url> opendb && cd opendb
cp .env.example .env
# .env faylini oching: SECRET_KEY, DB_PASSWORD, DJANGO_SUPERUSER_PASSWORD to'ldiring

docker compose up --build
```

Shu bilan tugadi. Birinchi ishga tushirishda konteyner avtomatik ravishda:
migratsiyalarni bajaradi, **barcha 3228 yozuvni yuklaydi**, superuser
yaratadi, va statik fayllarni yig'adi.

- API: http://localhost:8080/api/v1/
- Swagger hujjatlar: http://localhost:8080/api/docs/
- Admin panel: http://localhost:8080/admin/ (`.env`dagi DJANGO_SUPERUSER_* bilan kiring)

## Docker'siz lokal ishga tushirish (SQLite bilan)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # DB_HOST bo'sh qoldiring -- SQLite ishlatiladi
python manage.py migrate
python manage.py loaddata geo/fixtures/*.json
python manage.py createsuperuser
python manage.py runserver
```

## API endpointlari

Barchasi `GET /api/v1/...`, sahifalangan (`?page=2`), va filtrlanadigan:

```
viloyatlar/                    ?turi=viloyat|respublika|shahar
viloyatlar/<code>/             masalan UZ-TK
tumanlar/                      ?viloyat=<id>&turi=tuman|shahar
tumanlar/<slug>/
aholi-punktlari/                ?tuman=<id>
aholi-punktlari/<slug>/
banklar/                       ?turi=davlat|xususiy|...&viloyat=<id>
otmlar/                        ?turi=davlat&viloyat=<id>
valyutalar/                    -- har biri eng so'nggi kursi bilan
valyutalar/<code>/             masalan USD
valyuta-kurslari/               ?valyuta=<id>&sana=YYYY-MM-DD
bayramlar/                     ?turi=milliy|diniy
bayram-sanalari/                ?yil=2026
telefon-kodlari/                ?turi=mintaqaviy|mobil
namoz-vaqtlari/<viloyat_code>/  ?sana=YYYY-MM-DD (standart: bugun) -- HISOBLANADI, bazadan emas
```

## Valyuta kursini yangilash (qo'lda, Celery ulanmaguncha)

```bash
python manage.py sync_kurslar
```

CBU API'dan barcha valyutalarni qayta so'raydi va bugungi kursni yozadi
(`update_or_create` bilan -- xavfsiz, necha marta ishga tushirish mumkin).
Production'da buni cron yoki Celery beat orqali kuniga bir marta avtomatik
qilish kerak (`README`dagi izohga qarang).

## Muhim eslatmalar

- Ba'zi ma'lumotlar (Tuman, AholiPunkti, OTM) community/norasmiy manbalardan
  olingan va bir nechta o'zi tuzatilgan xato bor edi -- barchasi
  [`DATA_SOURCES.md`](./DATA_SOURCES.md)da ochiq hujjatlashtirilgan.
- Namoz vaqtlari burchagi (15°/15°) rasmiy hujjatdan emas, ikkita real
  sanaga moslashtirish orqali topilgan -- din bilan bog'liq jiddiy
  foydalanish uchun imom bilan tasdiqlash tavsiya etiladi.
