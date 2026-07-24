# Manba va tuzatishlar — Viloyat / Tuman

## Manba
- Bazaviy ma'lumot: [MIMAXUZ/uzbekistan-regions-data](https://github.com/MIMAXUZ/uzbekistan-regions-data)
  (community tomonidan yig'ilgan, oxirgi yangilanish 2025-04-16), o'zi SOATO/MHOBT'ga
  asoslangan deb da'vo qiladi.
- **Bu rasmiy davlat manbai emas.** Rasmiy asl manba —
  Davlat statistika qo'mitasining `soato(mhobt)_YYYY.xlsx` klassifikatori (stat.uz).
  Ushbu loyihada u to'g'ridan-to'g'ri fetch qilinmadi (tarmoq ruxsati yo'q edi).
- Cross-check: SOATO prefikslari (1703, 1727, 1730...) mustaqil ikkinchi manba —
  Sog'liqni saqlash vazirligi FHIR CodeSystem (build.fhir.org/ig/uzinfocom-org) — bilan
  mos kelishi tekshirildi.

## Qilingan tuzatishlar (207 -> 209 dan avval qo'lda ko'rib chiqilgan holatlar)
1. **1 ta axlat qator olib tashlandi**: "Toshkent shahrining tumanlari" (soato_id
   1726260260, 10 xonali, name_ru=null) — haqiqiy obyekt emas, manbadagi parsing xatosi.
2. **2 ta tuman SOATO kodisiz qoldirildi** (soato_code=null): Namangan viloyatidagi
   "Davlatobod tumani" va "Yangi Namangan tumani" — bular haqiqatda mavjud (Vikipediya
   orqali tasdiqlangan, mos ravishda 2020 va 2021-yilda tashkil etilgan, Namangan shahri
   tarkibida), lekin manbada SOATO kodi noto'g'ri formatda (10 xonali) edi. Xato kod
   yozishdan ko'ra bo'sh qoldirish afzal ko'rildi.
3. **1 ta nom tuzatildi**: "Baxt shaxar" -> "Baxt" (imlo xatosi + boshqa shahar
   yozuvlariga mos bo'lmagan ortiqcha so'z, Sirdaryo viloyati).
4. **Apostrof normalizatsiyasi**: manbada aralash ', ‘, ’ belgilari ishlatilgan,
   barchasi oddiy ' (U+0027) ga keltirildi.

## Ma'lum cheklovlar (keyingi bosqichda hal qilinishi mumkin)
- Toshkent shahri (12) va Namangan shahri (2: Davlatobod, Yangi Namangan) ICHIDAGI
  tumanlar hozircha to'g'ridan-to'g'ri viloyat/shahar-maqomiga bog'langan — 3-darajali
  ichma-ich ierarxiya (shahar -> o'z tumanlari) hali modellanmagan.
- `name_en` maydoni bo'sh qoldirildi — ishonchli inglizcha nom manbai keyinroq qo'shiladi.
- Tuman markazlari (masalan qaysi tuman markazi qaysi shahar) hali yo'q.

**Tavsiya**: production'ga chiqarishdan oldin, ayniqsa yangi tashkil etilgan tumanlar
bo'yicha, stat.uz'ning rasmiy xlsx fayli bilan bir marta qo'lda solishtirib chiqish
tavsiya etiladi.

---

## Aholi punkti (qishloq/shaharcha) darajasi

- Manba: xuddi shu repo'dagi `villages.json` (2,641 xom yozuv).
- **Bu MFY/mahalla emas.** Manbada mahalla darajasi 0 ta yozuv (README'da ochiq
  yozilgan: eskirgan Quarters jadvali olib tashlangan). Bu daraja "qishloq fuqarolar
  yig'ini" hududlari + shaharchalarga mos keladi -- ya'ni tumandan bir daraja past,
  mahalladan bir daraja yuqori.
- **Qishloq va shaharchani turi bo'yicha ajratib bo'lmadi** -- manbada faqat 10 ta
  yig'indi/sarlavha qatorida ("...shahar xokimiyatiga qarashli shaharchalar") so'z
  bor edi, ular chetlab o'tildi (haqiqiy joy emas). Qolgan 2,631 ta yozuvning
  qaysi biri qishloq, qaysi biri shaharcha -- bu ma'lumot yo'q, shu sababli
  `AholiPunkti` modelida `turi` maydoni qo'yilmadi (soxta klassifikatsiya
  qilishdan ko'ra yo'qligini ochiq aytish afzal).
- **277 ta nom to'qnashuvi** (bir xil nom, boshqa SOATO kod, masalan bitta tumanda
  ikkita "Jalabek") aniqlandi -- bular xato emas, real hodisa (SOATO ro'yxatida
  turli hududlarda bir xil nomli qishloqlar uchraydi). `slug` maydoni shu sabab
  to'qnashgan hollarda `nom-soatokod` shaklida generatsiya qilindi.
- **5 ta real tumanda 0 ta aholi punkti bor** (ehtimol manba to'liq emas, tuman
  o'zi mavjud emas degani emas): Tuproqqal'a (Xorazm), G'ozg'on (Navoiy),
  Ko'kdala (Qashqadaryo), Bandixon (Surxondaryo), Bo'zatov (Qoraqalpog'iston).
  Qolgan 11+2 ta 0-aholi-punktli tuman -- Toshkent va Namangan shaharlarining
  ICHKI (butunlay urban) tumanlari, ular uchun 0 ta qishloq bo'lishi normal.

---

## Bank

- Manba: **O'zbekiston Respublikasi Markaziy banki** (cbu.uz), "Tijorat
  banklarining bosh ofislari" sahifasi. Bu birinchi model bo'lib, community
  emas, to'g'ridan-to'g'ri rasmiy davlat manbaidan olindi. Saytdagi
  yangilanish sanasi: **06.07.2026** (juda yangi).
- 35 ta litsenziyaga ega bank: 9 davlat, 7 aksiyadorlik, 14 xususiy,
  5 chet el kapitali ishtirokidagi.
- **MFO kodi YO'Q.** O'zbekistonda MFO kodi bankka emas, filialga beriladi
  (har bir filial/shahobcha o'z MFOsiga ega, to'lov marshrutlash shu orqali
  ishlaydi). Bank sahifasida "Bank kodi" maydoni faqat filiallar bo'limida
  ko'rinadi. Agar MFO kerak bo'lsa -- bu alohida, ancha kattaroq ish (har bir
  bankning filiallar sahifasini alohida yig'ish kerak) -- keyingi bosqich
  sifatida `BankFilial` modeli taklif qilindi (models.py oxirida izohda).
- **Litsenziya sanalari** manbada asosan "11.01.1900" kabi ko'rinadi -- bu
  haqiqiy sana emas, CMS'ning "sana kiritilmagan" uchun standart qiymati.
  Shu sabab `license_date` maydoni umuman qo'shilmadi (faqat `license_number`
  bor). Yagona haqiqatga o'xshagan sana -- AVO BANK uchun 28.02.2025 (yangi
  litsenziya) -- lekin izchillik uchun bu ham modelga kiritilmadi.
  Kerak bo'lsa qo'shish oson.
- Bank manzilidan `viloyat` FK avtomatik aniqlandi (matn ichida "Toshkent
  shahri"/"Farg'ona viloyati"/"Andijon shahri" izlash orqali) -- 33 ta
  Toshkent shahrida, 1 tasi Farg'onada (Universal bank, Qo'qon), 1 tasi
  Andijonda (Hamkorbank).

---

## OTM (Oliy ta'lim muassasasi)

- Manba: **oliygoh.uz** (abituriyent portali) -- **rasmiy emas**. Rasmiy
  vazirlik sayti (edu.uz / Oliy ta'lim, fan va innovatsiyalar vazirligi)
  JS orqali render qilingani sabab statik ro'yxat bermadi.
- 2026 yil holatiga ko'ra O'zbekistonda **jami 201 ta OTM** bor (~yarmi
  davlat, undan ko'prog'i xususiy, ~15% xorijiy). Bu yerda faqat **136 ta
  DAVLAT OTM** bor -- xususiy va xorijiy OTMlar (~65 ta) **kiritilmagan**,
  chunki oliygoh.uz'ning bu sahifasi DTM/davlat granti qabuliga bog'liq
  bo'lgani uchun faqat davlat OTMlarini ko'rsatadi.
- **`viloyat` maydoni TAXMINIY.** Nomdagi shahar kalit so'zidan (masalan
  "Andijon", "Termiz") avtomatik topilgan, aniq manzil bilan tekshirilmagan.
  Kalit so'z topilmagan ~41 ta OTM avtomatik "Toshkent shahri"ga yozildi --
  bu ko'pchiligida to'g'ri (markaziy OTMlar shu yerda), lekin ba'zilari
  (masalan "Jamoat xavfsizligi universiteti", "Geologiya fanlari
  universiteti") uchun tasdiqlanmagan taxmin, xato bo'lishi mumkin.
- **Manbada sifat muammolari borligicha saqlandi** (o'zim "tuzatmadim",
  chunki qaysi versiya to'g'ri ekanini bila olmayman):
  - Bitta aniq **slug/nom nomuvofiqligi**: "Samarqand davlat veterinariya...
    Toshkent filiali" nomli qatorning slug'i `toshkent-temir-yo-l-transporti-
    muhandislari-instituti` (temir yo'l transporti!) -- bu ikkisi bir-biriga
    aloqasi yo'q narsalar, manbada aniq xato bor.
  - **4 ta nom boshqa-boshqa slug bilan takrorlanadi** (masalan "Toshkent
    davlat iqtisodiyot universiteti" 3 marta) -- bular so'nggi yillarda
    kichikroq institutlar yiriklariga qo'shib yuborilgan holatlar bo'lishi
    mumkin (masalan sobiq "Toshkent moliya instituti" endi "Toshkent davlat
    iqtisodiyot universiteti" deb ataladi, lekin eski yozuv alohida qolgan).
    Aniqlashtirish uchun rasmiy manba kerak.
  - Ba'zi "filial" qatorlar asosiy universitetga FK orqali bog'lanmagan --
    model darajasida `parent` maydoni yo'q (izohda taklif qilindi).
- **Tavsiya**: bu ro'yxatni "yakuniy" deb e'lon qilishdan oldin kamida
  yuqoridagi nomuvofiqliklarni edu.uz yoki rasmiy OTM reestri bilan
  solishtirish kerak. Xususiy+xorijiy OTMlar uchun alohida manba
  (ehtimol Kotirovka.uz yoki edu.uz'ning API/backend so'rovi) izlanishi kerak
  bo'ladi.

---

## Valyuta / Valyuta kursi

- Manba: **Markaziy bank rasmiy JSON API**
  (`cbu.uz/uz/arkhiv-kursov-valyut/json/`) -- eng ishonchli manba shu paytgacha,
  chunki bu boshqalar kabi HTML scraping emas, balki CBU'ning o'zi
  dasturchilar uchun chiqargan tayyor JSON.
- 74 ta valyuta, snapshot sanasi: **03.07.2026**.
- **Bu ikkalasi (`Bank`, `OTM`) dan tubdan farq qiladi**: statik seed emas,
  **kunlik yangilanadigan** ma'lumot. Shu sabab ikkiga bo'lindi:
  - `Valyuta` -- barqaror spravochnik (kod, nom, nominal)
  - `ValyutaKursi` -- har kuni yangi qator qo'shiladigan kurs tarixi,
    `(valyuta, sana)` bo'yicha unique constraint bilan
- `Nominal` maydoniga e'tibor: ba'zi valyutalar (VND, IDR, IRR) uchun kurs
  1 birlik uchun emas, 10 birlik uchun beriladi -- API shunday qaytaradi,
  hisob-kitobda buni hisobga olish kerak.
- `models.py` oxirida **ishlaydigan** Django management command namunasi
  bor (`sync_kurslar.py`) -- shu API'ni har kuni chaqirib, ikkala jadvalni
  ham yangilaydi (`update_or_create` bilan, xavfsiz qayta ishga tushirish
  mumkin). Production'da buni Celery beat yoki cronga ulash kerak bo'ladi.
- CBU API'sida tarixiy sana bo'yicha so'rov ham bor
  (`/json/all/YYYY-MM-DD/`), lekin sinovda eski sana so'ralganda ham eng
  so'nggi kurs qaytdi -- ehtimol keshlash yoki so'rov formatiga bog'liq,
  agar chinakam tarixiy backfill kerak bo'lsa alohida tekshirish talab
  qilinadi.

---

## Bayram / Bayram sanasi

- Manba: **Prezident Farmoni PF-257** (24.12.2025, "2026-yilda rasmiy
  sanalarni nishonlash davrida qo'shimcha ishlanmaydigan kunlarni belgilash
  va dam olish kunlarini ko'chirish to'g'risida") va **Mehnat kodeksi
  208-moddasi**. 4 mustaqil manba orqali tasdiqlangan: gov.uz (rasmiy
  hukumat portali), lex.uz (qonunchilik bazasi, hujjatning o'zi), norma.uz,
  kadrovik.uz -- bu hozirgacha eng yuqori ishonchlilik darajasidagi manba.
- 11 ta bayram ta'rifi (7 milliy dam olish kuni + 2 diniy + 2 nishonlanadigan-
  lekin-ish-kuni: Vatan himoyachilari kuni 14-yanvar, Bolalarni himoya qilish
  kuni 1-iyun), 2026-yil uchun 17 ta aniq sana yozuvi.
- **Diniy bayramlar (Ro'za hayit, Qurbon hayit) sanasi TAXMINIY**
  (`taxminiymi=True`) -- Oy taqvimiga asoslangan, yakuniy sana
  O'zbekiston musulmonlari idorasi tomonidan oy ko'rinishi tasdiqlangach
  e'lon qilinadi, ±1 kunga siljishi mumkin. 2026-yil uchun taxmin: Ro'za
  hayit 20-mart, Qurbon hayit 27-may.
- **Har yili yangilanishi kerak** -- xuddi valyuta kursi kabi, lekin kunlik
  emas, yiliga bir marta (odatda dekabr oxirida, kelasi yilgi Prezident
  farmoni chiqqanda). `BayramSanasi.yil` maydoni orqali bir nechta yil
  parallel saqlanishi mumkin.
- Diqqat: 6 kunlik va 5 kunlik ish haftasidagi xodimlar uchun ko'chirish
  qoidalari farq qiladi (masalan Navro'z va Xotira kuni 6-kunlik ish
  haftasida ishlaydiganlar uchun ko'chirilmaydi, chunki ularda shanba
  allaqachon ish kuni). Bu nuans modelda **hisobga olinmagan** -- barcha
  yozuvlar "standart 5-kunlik ish haftasi" nuqtai nazaridan berilgan
  (bu aksariyat foydalanuvchi uchun to'g'ri taxmin).

---

## Namoz vaqtlari

- **Bu boshqa hamma narsadan farqli** -- manba emas, balki HISOBLASH.
  Ma'lumot bazasidan olinmaydi, quyosh holati (NOAA formulasi) + joylashuv
  + sana asosida real vaqtda hisoblanadi. Foydalanuvchi avval xuddi shu
  yondashuvni Shom (Maghrib) uchun ishlatgan edi (`tez_soat.html`), bu
  yerda barcha 6 vaqtga (Bomdod/Quyosh/Peshin/Asr/Shom/Xufton) kengaytirildi.
- **Validatsiya usuli manba-sitatadan farq qiladi**: bu yerda "qaysi
  hujjatdan olindi" emas, "qanchalik aniq" muhim. Shu sabab natijani
  namozvaqti.uz'ning haqiqiy e'lon qilingan jadvali bilan **ikkita butunlay
  boshqa mavsumda** (24-iyul va 15-yanvar 2026, Toshkent) solishtirdim.
- **Muhim topilma**: standart global burchak (Jahon Musulmonlar Ligasi,
  18°/17°) mahalliy nashr bilan mos kelmadi (Bomdod ~20 daqiqa, Xufton
  ~17 daqiqa farq). Burchakni 15°/15° (ISNA-uslub) ga o'zgartirganda ikkala
  mavsumda ham farq 0-4 daqiqagacha tushdi. **Bu burchak biror rasmiy
  hujjatdan emas, ikkita nuqtaga moslashtirish (fitting) orqali topildi** --
  matematik jihatdan ishonchli, lekin O'zbekiston musulmonlari idorasining
  rasmiy metodologiya hujjatiga asoslanmagan (bunday hujjatni ochiq internetda
  topa olmadim). Agar din bilan bog'liq real foydalanish uchun ishlatilsa,
  imom yoki mahalliy masjid bilan tasdiqlash tavsiya etiladi.
- Asr uchun Hanafiy uslub (soya koeffitsiyenti=2) ishlatildi -- bu qism
  bir nechta mustaqil manba (namoz-vaqti.com'ning turli shahar sahifalari)
  tomonidan "O'zbekistonda keng qo'llanadigan usul" sifatida aniq
  tasdiqlangan, burchaklardan farqli o'laroq ancha ishonchli.
- `Viloyat` modeliga `latitude`/`longitude` qo'shildi (14 viloyat markazi) --
  bu Namoz vaqtlarini istalgan viloyat uchun hisoblashga imkon beradi.
  Koordinatalar umumiy geografik bilimdan (barqaror, qidiruv talab
  qilinmaydi), tekshirilmagan aniq manba yo'q, lekin shahar darajasidagi
  standart koordinatalar bo'lgani uchun xato ehtimoli juda past.
- `geo/namoz_hisoblash.py` -- to'liq ishlaydigan, sinovdan o'tgan modul.
  Diniy bayramlar (Ro'za/Qurbon hayit) singari, bu ham "taxminiy" toifaga
  kiradi -- lekin farqli o'laroq, tashqi e'londan emas, matematik
  hisob-kitobdan kelib chiqadi.

---

## Telefon kodlari

- 14 mintaqaviy (simli aloqa) kod, `Viloyat`ga bevosita bog'langan +
  13 mobil operator kodi.
- Manba: rasmiy 2014-yilgi 9-xonali raqamlash tizimiga o'tish farmoni haqida
  gazeta.uz yozuvi (geografik kodlar ro'yxati asosiy manba) +
  goldenpages.uz (aloqa yo'nalishi, tuman/shahar darajasida solishtirish
  uchun) + raqamtanlash.uz (OQ Mobile kabi yangi operatorlar uchun).
- **Muhim tuzatish**: Navoiy viloyati uchun bir nechta manba (jumladan
  goldenpages.uz'ning asosiy jadvali) "36" kodini ko'rsatadi -- bu **eski,
  2014-yilgacha bo'lgan kod** (o'sha paytda "436" formatida). 2014-yilgi
  rasmiy o'tish bilan Navoiy **maxsus ravishda** 79 kodiga o'tkazilgan
  (gazeta.uz: "Faqatgina Navoiy viloyatiga amaldagi 436 kodi o'rniga
  yangi — 79 kodi beriladi"), va bu Vikipediyaning Navoiy shahri
  sahifasida ("Area code: +998-79") mustaqil tasdiqlangan. Shu sabab bu
  yerda 79 ishlatildi -- eski manbalarga ko'r-ko'rona ergashilmadi.
- Mobil operatorlar: Beeline, Ucell, Mobiuz (avvalgi UMS), Perfectum
  Mobile, Uzmobile, Humans, va eng yangisi -- **OQ Mobile** (kod 20,
  O'zbekistondagi birinchi "raqamli" operator, 2020-yilgi eski
  ma'lumotnomalarda mavjud emas edi, alohida qidirib topildi).
- Chetlab o'tilgan: alternativ simli aloqa operatorlari (Buzton, East
  Telecom, Sarkor Telecom, Sharq Telecom) kodi 78 -- bular geografik yoki
  yagona operator kodi emas, balki "muqobil simli operator" toifasi,
  hozircha modelga kiritilmadi (kerak bo'lsa `turi` ga uchinchi variant
  sifatida qo'shish oson).







