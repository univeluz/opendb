"""
django-import-export uchun resurslar -- admin panelida CSV/JSON/XLSX
import va eksport qilish imkonini beradi (har bir model uchun "Import"/
"Export" tugmalari admin.py orqali ImportExportModelAdmin'ga ulanadi).
"""
from import_export import resources
from .models import (
    Viloyat, Tuman, AholiPunkti, Bank, OTM,
    Valyuta, ValyutaKursi, Bayram, BayramSanasi, TelefonKodi,
)


class ViloyatResource(resources.ModelResource):
    class Meta:
        model = Viloyat


class TumanResource(resources.ModelResource):
    class Meta:
        model = Tuman


class AholiPunktiResource(resources.ModelResource):
    class Meta:
        model = AholiPunkti


class BankResource(resources.ModelResource):
    class Meta:
        model = Bank


class OTMResource(resources.ModelResource):
    class Meta:
        model = OTM


class ValyutaResource(resources.ModelResource):
    class Meta:
        model = Valyuta


class ValyutaKursiResource(resources.ModelResource):
    class Meta:
        model = ValyutaKursi


class BayramResource(resources.ModelResource):
    class Meta:
        model = Bayram


class BayramSanasiResource(resources.ModelResource):
    class Meta:
        model = BayramSanasi


class TelefonKodiResource(resources.ModelResource):
    class Meta:
        model = TelefonKodi
