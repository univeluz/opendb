# CLAUDE.md — OpenDB (opendb.uz)

O'zbekiston uchun ochiq ma'lumotlar API'si. Bu loyiha claude.ai chatida
bosqichma-bosqich qurilgan (Django modellari → ma'lumot yig'ish → Docker
paketlash), endi shu yerda (Claude Code) davom ettirilmoqda: Docker'ni
ishga tushirish, .env'ni to'ldirish, GitHub'ga push qilish.

To'liq kontekst uchun (avval shularni o'qi):
@README.md
@DATA_SOURCES.md

## Hozirgi holat -- MUHIM

- **Django ilovasi to'liq test qilingan**: 10 model, 3228 yozuv, barcha
  `/api/v1/...` endpointlar SQLite ustida real HTTP so'rovlar bilan
  tekshirilgan (natijalar README'da).
- **Docker hech qachon haqiqiy docker ustida ishga tushirilmagan.**
  Yozilgan muhitda (claude.ai sandbox) docker daemon yo'q edi -- shu sabab
  `Dockerfile`/`docker-compose.yml` faqat YAML/shell sintaksisi
  tekshirilgan, konteyner qurilishi tasdiqlanmagan. Birinchi
  `docker compose up`da kutilmagan xato chiqsa -- bu normal, sabab shu.
  Eng ehtimoliy joylar: `entrypoint.sh`ning executable biti (git ba'zan
  yo'qotadi), Postgres healthcheck vaqti yetarli emasligi, yoki
  requirements.txt'dagi versiyalarning bazaviy image bilan mos kelmasligi.

## Vazifa -- ketma-ket bajar

1. `.env.example`dan `.env` yasa. `SECRET_KEY`ni generate qil
   (`python -c "import secrets; print(secrets.token_urlsafe(50))"`),
   `DB_PASSWORD` va `DJANGO_SUPERUSER_PASSWORD`ni tasodifiy kuchli
   qiymatlar bilan to'ldir. **`.env` HECH QACHON commit qilinmasin** --
   `.gitignore`da borligini tekshir.
2. `docker compose up --build` ishga tushir, loglarni kuzat. `web`
   konteyneri `entrypoint.sh` orqali: DB kutadi → migratsiya → 10 ta
   fixture yuklaydi (~3228 yozuv) → superuser yaratadi → collectstatic →
   gunicorn. Shu ketma-ketlikning qaysi bosqichida xato chiqishini top.
3. Xato chiqsa tuzat (odatda kichik -- yuqoridagi ro'yxatga qara).
4. Ishga tushgach tekshir:
   - `curl localhost:8080/api/v1/viloyatlar/UZ-TK/`
   - `curl localhost:8080/api/v1/namoz-vaqtlari/UZ-TK/`
   - `localhost:8080/admin/` (.env'dagi DJANGO_SUPERUSER_* bilan)
   - `localhost:8080/api/docs/` (Swagger)
5. `git status` va `git remote -v` bilan holatni ko'r (remote allaqachon
   ulangan bo'lishi kerak, foydalanuvchi tasdiqladi). Keyin `git add`,
   ma'noli commit xabari bilan commit, va push qil.

## Arxitektura qarorlari (chatda muhokama qilingan, qisqacha)

- **ID strategiyasi**: barcha ochiq ma'lumot (Viloyat...TelefonKodi)
  oddiy `BigAutoField` ishlatadi -- bu ochiq API uchun muammo emas,
  hatto foydali (pagination). UUID faqat KELAJAKDA qo'shiladigan
  APIKey/Client modeliga mo'ljallangan (hali yo'q).
- **API hozircha faqat o'qish uchun** (`ReadOnlyModelViewSet`) -- yozish
  faqat admin panel orqali (jazzmin + import-export).
- **Rate limit** allaqachon ulangan: `AnonRateThrottle`,
  `.env`dagi `ANON_THROTTLE_RATE` orqali sozlanadi (standart 1000/kun).
- **Namoz vaqtlari bazada saqlanmaydi** -- har so'rovda hisoblanadi
  (`geo/namoz_hisoblash.py`, NOAA formulasi).
- **Valyuta kursi statik emas** -- `sync_kurslar` management command bor,
  hali avtomatik jadval (cron/Celery) ulanmagan.
- Toshkent shahri/Namangan shahri kabi ba'zi shaharlarning ICHKI
  tumanlari bor -- bu 3-darajali ierarxiya hali modellanmagan, `Tuman`
  ularni to'g'ridan-to'g'ri viloyatga bog'laydi (DATA_SOURCES.md'da bor).

## Keyingi bosqichlar (loyihaning o'zi, Docker emas)

Redis, Celery, JWT, Nginx, CI/CD -- ataylab hali yo'q (README'da sabab
yozilgan). Xususiy/xorijiy OTMlar, mahalla (MFY) darajasi, bank
filiallari/MFO -- hali yig'ilmagan, DATA_SOURCES.md'da har biri uchun
"keyingi qadam" izohi bor.
