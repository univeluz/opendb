from rest_framework import serializers
from .models import (
    Viloyat, Tuman, AholiPunkti, Bank, OTM,
    Valyuta, ValyutaKursi, Bayram, BayramSanasi, TelefonKodi,
)


class ViloyatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viloyat
        fields = [
            "id", "code", "soato_code", "name_uz", "name_uz_cyrl", "name_ru", "name_en",
            "center", "turi", "latitude", "longitude",
        ]


class TumanSerializer(serializers.ModelSerializer):
    viloyat_nomi = serializers.CharField(source="viloyat.name_uz", read_only=True)

    class Meta:
        model = Tuman
        fields = [
            "id", "viloyat", "viloyat_nomi", "slug", "soato_code",
            "name_uz", "name_uz_cyrl", "name_ru", "name_en", "turi",
        ]


class AholiPunktiSerializer(serializers.ModelSerializer):
    tuman_nomi = serializers.CharField(source="tuman.name_uz", read_only=True)
    viloyat_nomi = serializers.CharField(source="tuman.viloyat.name_uz", read_only=True)

    class Meta:
        model = AholiPunkti
        fields = [
            "id", "tuman", "tuman_nomi", "viloyat_nomi", "slug", "soato_code",
            "name_uz", "name_uz_cyrl", "name_ru", "name_en",
        ]


class BankSerializer(serializers.ModelSerializer):
    viloyat_nomi = serializers.CharField(source="viloyat.name_uz", read_only=True, default=None)

    class Meta:
        model = Bank
        fields = [
            "id", "slug", "name_uz", "turi", "viloyat", "viloyat_nomi",
            "address", "license_number", "website",
        ]


class OTMSerializer(serializers.ModelSerializer):
    viloyat_nomi = serializers.CharField(source="viloyat.name_uz", read_only=True, default=None)

    class Meta:
        model = OTM
        fields = ["id", "slug", "name_uz", "turi", "viloyat", "viloyat_nomi", "source_url"]


class ValyutaSerializer(serializers.ModelSerializer):
    oxirgi_kurs = serializers.SerializerMethodField()

    class Meta:
        model = Valyuta
        fields = [
            "id", "code", "iso_numeric_code", "name_uz", "name_uz_cyrl",
            "name_ru", "name_en", "nominal", "oxirgi_kurs",
        ]

    def get_oxirgi_kurs(self, obj) -> dict | None:
        kurs = obj.kurslar.first()  # ValyutaKursi.Meta.ordering = ["-sana", ...]
        if not kurs:
            return None
        return {"sana": kurs.sana, "rate": str(kurs.rate), "diff": str(kurs.diff)}


class ValyutaKursiSerializer(serializers.ModelSerializer):
    valyuta_kodi = serializers.CharField(source="valyuta.code", read_only=True)

    class Meta:
        model = ValyutaKursi
        fields = ["id", "valyuta", "valyuta_kodi", "sana", "rate", "diff"]


class BayramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bayram
        fields = [
            "id", "slug", "name_uz", "turi", "oy", "kun",
            "rasman_dam_olish_kuni", "tavsif",
        ]


class BayramSanasiSerializer(serializers.ModelSerializer):
    bayram_nomi = serializers.CharField(source="bayram.name_uz", read_only=True)

    class Meta:
        model = BayramSanasi
        fields = ["id", "bayram", "bayram_nomi", "yil", "sana", "sabab", "taxminiymi", "izoh"]


class TelefonKodiSerializer(serializers.ModelSerializer):
    viloyat_nomi = serializers.CharField(source="viloyat.name_uz", read_only=True, default=None)

    class Meta:
        model = TelefonKodi
        fields = ["id", "kodi", "turi", "viloyat", "viloyat_nomi", "operator_nomi"]


class NamozVaqtlariSerializer(serializers.Serializer):
    """Bazadan emas -- hisoblab chiqarilgan natija uchun (model emas)."""
    viloyat = serializers.CharField()
    sana = serializers.DateField()
    bomdod = serializers.CharField()
    quyosh = serializers.CharField()
    peshin = serializers.CharField()
    asr = serializers.CharField()
    shom = serializers.CharField()
    xufton = serializers.CharField()
