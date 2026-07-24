from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Viloyat, Tuman, AholiPunkti, Bank, OTM,
    Valyuta, ValyutaKursi, Bayram, BayramSanasi, TelefonKodi,
)
from .resources import (
    ViloyatResource, TumanResource, AholiPunktiResource, BankResource, OTMResource,
    ValyutaResource, ValyutaKursiResource, BayramResource, BayramSanasiResource,
    TelefonKodiResource,
)


@admin.register(Viloyat)
class ViloyatAdmin(ImportExportModelAdmin):
    resource_classes = [ViloyatResource]
    list_display = ["name_uz", "code", "turi", "center", "soato_code"]
    list_filter = ["turi"]
    search_fields = ["name_uz", "name_ru", "code", "soato_code"]


@admin.register(Tuman)
class TumanAdmin(ImportExportModelAdmin):
    resource_classes = [TumanResource]
    list_display = ["name_uz", "viloyat", "turi", "soato_code"]
    list_filter = ["turi", "viloyat"]
    search_fields = ["name_uz", "name_ru", "soato_code", "slug"]
    autocomplete_fields = ["viloyat"]


@admin.register(AholiPunkti)
class AholiPunktiAdmin(ImportExportModelAdmin):
    resource_classes = [AholiPunktiResource]
    list_display = ["name_uz", "tuman", "soato_code"]
    list_filter = ["tuman__viloyat"]
    search_fields = ["name_uz", "name_ru", "soato_code", "slug"]
    autocomplete_fields = ["tuman"]


@admin.register(Bank)
class BankAdmin(ImportExportModelAdmin):
    resource_classes = [BankResource]
    list_display = ["name_uz", "turi", "viloyat", "license_number", "website"]
    list_filter = ["turi", "viloyat"]
    search_fields = ["name_uz", "license_number"]
    autocomplete_fields = ["viloyat"]


@admin.register(OTM)
class OTMAdmin(ImportExportModelAdmin):
    resource_classes = [OTMResource]
    list_display = ["name_uz", "turi", "viloyat"]
    list_filter = ["turi", "viloyat"]
    search_fields = ["name_uz"]
    autocomplete_fields = ["viloyat"]


@admin.register(Valyuta)
class ValyutaAdmin(ImportExportModelAdmin):
    resource_classes = [ValyutaResource]
    list_display = ["code", "name_uz", "nominal"]
    search_fields = ["code", "name_uz", "name_ru"]


@admin.register(ValyutaKursi)
class ValyutaKursiAdmin(ImportExportModelAdmin):
    resource_classes = [ValyutaKursiResource]
    list_display = ["valyuta", "sana", "rate", "diff"]
    list_filter = ["sana"]
    autocomplete_fields = ["valyuta"]
    date_hierarchy = "sana"


@admin.register(Bayram)
class BayramAdmin(ImportExportModelAdmin):
    resource_classes = [BayramResource]
    list_display = ["name_uz", "turi", "oy", "kun", "rasman_dam_olish_kuni"]
    list_filter = ["turi", "rasman_dam_olish_kuni"]
    search_fields = ["name_uz"]


@admin.register(BayramSanasi)
class BayramSanasiAdmin(ImportExportModelAdmin):
    resource_classes = [BayramSanasiResource]
    list_display = ["bayram", "yil", "sana", "sabab", "taxminiymi"]
    list_filter = ["yil", "sabab", "taxminiymi"]
    autocomplete_fields = ["bayram"]
    date_hierarchy = "sana"


@admin.register(TelefonKodi)
class TelefonKodiAdmin(ImportExportModelAdmin):
    resource_classes = [TelefonKodiResource]
    list_display = ["kodi", "turi", "viloyat", "operator_nomi"]
    list_filter = ["turi"]
    autocomplete_fields = ["viloyat"]
