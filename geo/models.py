from django.db import models


class Viloyat(models.Model):
    """
    O'zbekiston viloyatlari (12 viloyat + Qoraqalpog'iston Respublikasi + Toshkent shahri).
    Manba: ISO 3166-2:UZ (barqaror kod) + Davlat statistika qo'mitasi SOATO/MHOBT (rasmiy kod).
    """

    class Turi(models.TextChoices):
        VILOYAT = "viloyat", "Viloyat"
        RESPUBLIKA = "respublika", "Respublika"
        SHAHAR = "shahar", "Shahar"

    code = models.CharField(
        max_length=5, unique=True, db_index=True,
        help_text="ISO 3166-2:UZ kodi, masalan UZ-TK",
    )
    soato_code = models.CharField(
        max_length=10, unique=True, null=True, blank=True,
        help_text="Davlat statistika qo'mitasi rasmiy SOATO/MHOBT kodi",
    )
    name_uz = models.CharField(max_length=100)
    name_uz_cyrl = models.CharField(max_length=100, blank=True)
    name_ru = models.CharField(max_length=100, blank=True)
    name_en = models.CharField(max_length=100, blank=True)
    center = models.CharField(max_length=100, blank=True, help_text="Markaz shahri")
    turi = models.CharField(max_length=12, choices=Turi.choices, default=Turi.VILOYAT)
    latitude = models.DecimalField(
        max_digits=8, decimal_places=5, null=True, blank=True,
        help_text="Markaz shahrining kengligi -- namoz vaqti va shunga o'xshash hisob-kitoblar uchun",
    )
    longitude = models.DecimalField(
        max_digits=8, decimal_places=5, null=True, blank=True,
        help_text="Markaz shahrining uzunligi",
    )

    class Meta:
        db_table = "viloyatlar"
        ordering = ["name_uz"]
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"

    def __str__(self):
        return self.name_uz


class Tuman(models.Model):
    """
    Tuman (rayon) va viloyat/respublika bo'ysunuvidagi shaharlar (masalan Nurafshon, Angren).
    Bittasi ikkinchisining pastki turi emas -- ikkalasi ham viloyatga bevosita bo'ysunadigan,
    bir xil ierarxik darajadagi ma'muriy birliklar, shu sababli bitta modelda `turi` maydoni
    bilan ajratiladi.

    Diqqat: Toshkent va Namangan shaharlari o'zining ICHKI tumanlariga ega (Chilonzor,
    Yunusobod, Davlatobod va h.k.) -- bu yozuvlar shu shaharning tegishli viloyatiga (yoki
    Toshkent shahri holida, shahar-viloyat maqomiga) bog'langan, chunki hozircha 3-darajali
    ichma-ich (shahar -> tuman) ierarxiya modellanmagan. Kerak bo'lsa keyinroq qo'shiladi.
    """

    class Turi(models.TextChoices):
        TUMAN = "tuman", "Tuman"
        SHAHAR = "shahar", "Shahar (viloyat bo'ysunuvidagi)"

    viloyat = models.ForeignKey(Viloyat, on_delete=models.CASCADE, related_name="tumanlar")
    slug = models.SlugField(
        max_length=120, unique=True,
        help_text="URL uchun, masalan 'oltinkol-tumani'",
    )
    soato_code = models.CharField(
        max_length=12, unique=True, null=True, blank=True,
        help_text="Davlat statistika qo'mitasi SOATO/MHOBT kodi. "
                   "Ba'zi yangi tumanlar uchun manbada kod buzilgan bo'lgani sabab null.",
    )
    name_uz = models.CharField(max_length=100)
    name_uz_cyrl = models.CharField(max_length=100, blank=True)
    name_ru = models.CharField(max_length=100, blank=True)
    name_en = models.CharField(max_length=100, blank=True)
    turi = models.CharField(max_length=6, choices=Turi.choices)

    class Meta:
        db_table = "tumanlar"
        ordering = ["viloyat", "name_uz"]
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"
        constraints = [
            models.UniqueConstraint(fields=["viloyat", "name_uz"], name="uniq_tuman_per_viloyat"),
        ]

    def __str__(self):
        return f"{self.name_uz} ({self.viloyat.name_uz})"


class AholiPunkti(models.Model):
    """
    Tumandan pastki daraja: qishloq va shaharchalar.

    MUHIM CHEKLOV: bu MFY/mahalla (eng quyi, ko'cha darajasidagi) emas.
    Manba datasetida mahalla (MFY) ma'lumotlari yo'q (0 ta yozuv, eskirgan deb
    belgilanib olib tashlangan). Bu daraja rasman "qishloq fuqarolar yig'ini"
    hududlari va shaharchalarga mos keladi.

    Shuningdek: manbada qishloq va shaharchani nom bo'yicha aniq ajratib bo'lmadi
    (faqat yig'indi/sarlavha qatorlarda "shaharcha" so'zi bor edi, ular chetlab
    o'tildi) -- shu sababli bu yerda tuman.turi kabi `turi` maydoni YO'Q. Aniqlash
    uchun rasmiy SOATO xlsx kerak bo'ladi.
    """

    tuman = models.ForeignKey(Tuman, on_delete=models.CASCADE, related_name="aholi_punktlari")
    slug = models.SlugField(max_length=140, unique=True)
    soato_code = models.CharField(max_length=12, unique=True)
    name_uz = models.CharField(max_length=150)
    name_uz_cyrl = models.CharField(max_length=150, blank=True)
    name_ru = models.CharField(max_length=150, blank=True)
    name_en = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = "aholi_punktlari"
        ordering = ["tuman", "name_uz"]
        verbose_name = "Aholi punkti"
        verbose_name_plural = "Aholi punktlari"

    def __str__(self):
        return f"{self.name_uz} ({self.tuman.name_uz})"


# Keyingi bosqich uchun (haqiqiy MFY/mahalla ma'lumoti topilsa):
#
# class Mahalla(models.Model):
#     aholi_punkti = models.ForeignKey(AholiPunkti, on_delete=models.CASCADE, related_name="mahallalar")
#     code = models.CharField(max_length=15, unique=True)
#     name_uz = models.CharField(max_length=150)
#     ...


class Bank(models.Model):
    """
    O'zbekistonda litsenziyaga ega tijorat banklari (bosh ofislar darajasida).

    Manba: O'zbekiston Respublikasi Markaziy banki, "Tijorat banklarining bosh
    ofislari" sahifasi (cbu.uz/uz/credit-organizations/banks/head-offices/),
    saytda ko'rsatilgan yangilanish sanasi: 06.07.2026.

    DIQQAT: bu yerda MFO (bank filiali kodi) YO'Q -- O'zbekistonda MFO kodi
    bankka emas, balki HAR BIR FILIALGA alohida beriladi (to'lov marshrutlash
    uchun). MFO kerak bo'lsa, alohida BankFilial modeli va "Tijorat banklarining
    filiallari" manbai kerak bo'ladi (bu yerda yo'q, keyingi bosqich).
    """

    class Turi(models.TextChoices):
        DAVLAT = "davlat", "Davlat banki"
        AKSIYADORLIK = "aksiyadorlik", "Aksiyadorlik tijorat banki"
        XUSUSIY = "xususiy", "Xususiy bank"
        XORIJIY = "xorijiy", "Chet el kapitali ishtirokidagi bank"

    slug = models.SlugField(max_length=100, unique=True)
    name_uz = models.CharField(max_length=200)
    turi = models.CharField(max_length=14, choices=Turi.choices)
    viloyat = models.ForeignKey(
        Viloyat, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="banklar", help_text="Bosh ofis joylashgan viloyat",
    )
    address = models.CharField(max_length=300, help_text="Bosh ofis manzili (xom matn)")
    license_number = models.CharField(max_length=10, blank=True)
    website = models.URLField(blank=True)

    class Meta:
        db_table = "banklar"
        ordering = ["name_uz"]
        verbose_name = "Bank"
        verbose_name_plural = "Banklar"

    def __str__(self):
        return self.name_uz


# Keyingi bosqich uchun (filiallar/MFO kerak bo'lsa):
#
# class BankFilial(models.Model):
#     bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="filiallar")
#     tuman = models.ForeignKey(Tuman, on_delete=models.SET_NULL, null=True)
#     mfo_code = models.CharField(max_length=5, unique=True)
#     address = models.CharField(max_length=300)
#     ...


class OTM(models.Model):
    """
    Oliy ta'lim muassasalari (universitet, institut, akademiya).

    HOZIRCHA FAQAT DAVLAT OTMlari (~136 ta). Manba: oliygoh.uz (norasmiy,
    abituriyent portali -- rasmiy vazirlik sayti edu.uz JS orqali render
    qilingani sabab statik matn bermadi). O'zbekistonda jami 201 ta OTM bor
    (2026), demak xususiy (~90) va xorijiy (~30) OTMlar bu ro'yxatda YO'Q --
    alohida bosqich kerak.

    `viloyat` maydoni TAXMINIY -- nomdagi shahar kalit so'zidan avtomatik
    aniqlangan, tekshirilmagan. Aniq manzil kerak bo'lsa qo'lda tekshirish
    tavsiya etiladi (xususan Toshkent shahriga tushib qolgan ~41 tasi orasida
    haqiqatda boshqa hududda joylashganlari bo'lishi mumkin).

    `turi` -- filial/fakultet/asosiy universitet farqi model darajasida
    ajratilmagan (masalan "X universiteti Y filiali" alohida qator, lekin
    asosiy universitetga FK orqali bog'lanmagan). Kerak bo'lsa `parent`
    o'z-o'ziga FK sifatida keyinroq qo'shilishi mumkin.
    """

    class Turi(models.TextChoices):
        DAVLAT = "davlat", "Davlat OTM"
        XUSUSIY = "xususiy", "Xususiy OTM"
        XORIJIY = "xorijiy", "Xorijiy OTM filiali"

    slug = models.SlugField(max_length=200, unique=True)
    name_uz = models.CharField(max_length=300)
    turi = models.CharField(max_length=8, choices=Turi.choices, default=Turi.DAVLAT)
    viloyat = models.ForeignKey(
        Viloyat, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="otmlar", help_text="TAXMINIY -- nomdan avtomatik aniqlangan, tasdiqlanmagan",
    )
    source_url = models.URLField(blank=True)

    class Meta:
        db_table = "otmlar"
        ordering = ["name_uz"]
        verbose_name = "OTM"
        verbose_name_plural = "OTMlar"

    def __str__(self):
        return self.name_uz


# Keyingi bosqich uchun (xususiy/xorijiy OTMlar, aniq manzil, parent-filial bog'lanishi):
#
# class OTM(models.Model):
#     ...
#     parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="filiallar")
#     address = models.CharField(max_length=300, blank=True)
#     website = models.URLField(blank=True)


class Valyuta(models.Model):
    """
    Valyuta spravochnigi (barqaror -- kod/nom o'zgarmaydi, faqat kurs o'zgaradi).
    Manba: Markaziy bank rasmiy JSON API (cbu.uz/uz/arkhiv-kursov-valyut/json/).
    """

    cbu_id = models.PositiveSmallIntegerField(unique=True, help_text="CBU tizimidagi ichki id")
    iso_numeric_code = models.CharField(max_length=3, help_text="ISO 4217 raqamli kod, masalan 840=USD")
    code = models.CharField(max_length=3, unique=True, db_index=True, help_text="3 harfli kod, masalan USD")
    name_uz = models.CharField(max_length=100)
    name_uz_cyrl = models.CharField(max_length=100, blank=True)
    name_ru = models.CharField(max_length=100, blank=True)
    name_en = models.CharField(max_length=100, blank=True)
    nominal = models.PositiveSmallIntegerField(
        default=1, help_text="Kurs shuncha birlik uchun beriladi (masalan VND uchun 10)",
    )

    class Meta:
        db_table = "valyutalar"
        ordering = ["code"]
        verbose_name = "Valyuta"
        verbose_name_plural = "Valyutalar"

    def __str__(self):
        return self.code


class ValyutaKursi(models.Model):
    """
    Kunlik kurs -- HAR KUNI YANGI QATOR qo'shiladigan jadval, statik seed emas.
    Bitta valyuta uchun bir kunda faqat bitta kurs (unique_together).

    Production'da bu jadval Django management command orqali har kuni
    (masalan Celery beat yoki cron bilan) CBU API'dan yangilanishi kerak --
    quyida shunday komanda namunasi bor.
    """

    valyuta = models.ForeignKey(Valyuta, on_delete=models.CASCADE, related_name="kurslar")
    sana = models.DateField(db_index=True)
    rate = models.DecimalField(max_digits=12, decimal_places=2, help_text="1 (yoki nominal) birlik = shuncha so'm")
    diff = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Oldingi kunga nisbatan farq")

    class Meta:
        db_table = "valyuta_kurslari"
        ordering = ["-sana", "valyuta__code"]
        verbose_name = "Valyuta kursi"
        verbose_name_plural = "Valyuta kurslari"
        constraints = [
            models.UniqueConstraint(fields=["valyuta", "sana"], name="uniq_kurs_per_kun"),
        ]

    def __str__(self):
        return f"{self.valyuta.code} {self.sana}: {self.rate}"


# Kunlik sync uchun namuna: geo/management/commands/sync_kurslar.py
#
# import requests
# from datetime import datetime
# from django.core.management.base import BaseCommand
# from geo.models import Valyuta, ValyutaKursi
#
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         data = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
#         for item in data:
#             valyuta, _ = Valyuta.objects.update_or_create(
#                 cbu_id=item["id"],
#                 defaults=dict(
#                     iso_numeric_code=item["Code"], code=item["Ccy"],
#                     name_uz=item["CcyNm_UZ"], name_uz_cyrl=item["CcyNm_UZC"],
#                     name_ru=item["CcyNm_RU"], name_en=item["CcyNm_EN"],
#                     nominal=int(item["Nominal"]),
#                 ),
#             )
#             ValyutaKursi.objects.update_or_create(
#                 valyuta=valyuta,
#                 sana=datetime.strptime(item["Date"], "%d.%m.%Y").date(),
#                 defaults=dict(rate=item["Rate"], diff=item["Diff"]),
#             )
#
# Rejalashtirish: Celery beat bilan har kuni soat 12:00 da (CBU shu atrofda
# yangilaydi), yoki oddiy cron: `0 12 * * * python manage.py sync_kurslar`


class Bayram(models.Model):
    """
    Bayram TA'RIFI -- o'zgarmas (nomi, turi, milliy bayramlar uchun oy/kun).
    Diniy (oy taqvimiga asoslangan) bayramlar uchun oy/kun YO'Q -- ular har
    yili siljiydi, aniq sana faqat BayramSanasi'da, yiliga alohida.
    """

    class Turi(models.TextChoices):
        MILLIY = "milliy", "Milliy/qonuniy bayram"
        DINIY = "diniy", "Diniy bayram (oy taqvimi, har yili siljiydi)"

    slug = models.SlugField(max_length=100, unique=True)
    name_uz = models.CharField(max_length=150)
    turi = models.CharField(max_length=6, choices=Turi.choices)
    oy = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Faqat milliy bayramlar uchun (1-12)")
    kun = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Faqat milliy bayramlar uchun (1-31)")
    rasman_dam_olish_kuni = models.BooleanField(
        default=True, help_text="False bo'lsa -- nishonlanadi, lekin ish kuni (masalan Vatan himoyachilari kuni)",
    )
    tavsif = models.TextField(blank=True)

    class Meta:
        db_table = "bayramlar"
        ordering = ["oy", "kun"]
        verbose_name = "Bayram"
        verbose_name_plural = "Bayramlar"

    def __str__(self):
        return self.name_uz


class BayramSanasi(models.Model):
    """
    Bayramning MA'LUM BIR YILDAGI aniq sanasi -- statik emas, yiliga yangilanadi.

    Bitta bayram bir yilda BIR NECHA qator hosil qilishi mumkin: asosiy kun +
    ko'chirilgan/qo'shimcha kun(lar) (masalan 2026: Xotin-qizlar kuni ->
    8-mart (asosiy, yakshanbaga to'g'ri keldi) + 9-mart (MK 208-modda
    asosida ko'chirilgan dam olish)).

    Manba: Prezident Farmoni PF-257 (24.12.2025) va Mehnat Kodeksi 208-modda.
    Diniy bayramlar sanasi TAXMINIY -- yakuniy sana O'zbekiston musulmonlari
    idorasi tomonidan oy ko'rinishi tasdiqlangач e'lon qilinadi, ±1 kunga
    siljishi mumkin.
    """

    class SababTuri(models.TextChoices):
        ASOSIY = "asosiy", "Asosiy kun"
        KOCHIRILGAN = "kochirilgan", "MK 208-modda: dam kuniga to'g'ri kelgani uchun ko'chirilgan"
        QOSHIMCHA = "qoshimcha", "Prezident farmoni asosida qo'shimcha"

    bayram = models.ForeignKey(Bayram, on_delete=models.CASCADE, related_name="sanalar")
    yil = models.PositiveSmallIntegerField(db_index=True)
    sana = models.DateField()
    sabab = models.CharField(max_length=12, choices=SababTuri.choices, default=SababTuri.ASOSIY)
    taxminiymi = models.BooleanField(default=False, help_text="Diniy bayramlar uchun True")
    izoh = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "bayram_sanalari"
        ordering = ["sana"]
        verbose_name = "Bayram sanasi"
        verbose_name_plural = "Bayram sanalari"
        constraints = [
            models.UniqueConstraint(fields=["bayram", "sana"], name="uniq_bayram_sana"),
        ]

    def __str__(self):
        return f"{self.bayram.name_uz} -- {self.sana}"


class TelefonKodi(models.Model):
    """
    Telefon kodlari -- mintaqaviy (shahar/viloyat, simli aloqa) va mobil
    operator kodlari.

    Manba: rasmiy 2014-yilgi 9-xonali raqamlash tizimiga o'tish farmoni
    (gazeta.uz orqali tasdiqlangan) + goldenpages.uz. DIQQAT: Navoiy viloyati
    uchun ba'zi manbalarda "36" ko'rinadi -- bu ESKI (2014-yilgacha) kod,
    rasmiy ravishda 79 bilan almashtirilgan (Vikipediya orqali mustaqil
    tasdiqlangan). Shu sabab bu yerda 79 ishlatilgan, 36 emas.
    """

    class Turi(models.TextChoices):
        MINTAQAVIY = "mintaqaviy", "Mintaqaviy (simli aloqa)"
        MOBIL = "mobil", "Mobil operator"

    kodi = models.CharField(max_length=3, db_index=True)
    turi = models.CharField(max_length=10, choices=Turi.choices)
    viloyat = models.ForeignKey(
        Viloyat, on_delete=models.CASCADE, null=True, blank=True,
        related_name="telefon_kodlari", help_text="Faqat turi=mintaqaviy uchun",
    )
    operator_nomi = models.CharField(max_length=50, blank=True, help_text="Faqat turi=mobil uchun")

    class Meta:
        db_table = "telefon_kodlari"
        ordering = ["turi", "kodi"]
        verbose_name = "Telefon kodi"
        verbose_name_plural = "Telefon kodlari"
        constraints = [
            models.UniqueConstraint(fields=["kodi", "operator_nomi"], name="uniq_kod_operator"),
        ]

    def __str__(self):
        egasi = self.viloyat.name_uz if self.viloyat_id else self.operator_nomi
        return f"+998 {self.kodi} ({egasi})"
