from datetime import date as date_cls

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import (
    Viloyat, Tuman, AholiPunkti, Bank, OTM,
    Valyuta, ValyutaKursi, Bayram, BayramSanasi, TelefonKodi,
)
from .serializers import (
    ViloyatSerializer, TumanSerializer, AholiPunktiSerializer, BankSerializer, OTMSerializer,
    ValyutaSerializer, ValyutaKursiSerializer, BayramSerializer, BayramSanasiSerializer,
    TelefonKodiSerializer, NamozVaqtlariSerializer,
)
from .namoz_hisoblash import namoz_vaqtlari


class ViloyatViewSet(viewsets.ReadOnlyModelViewSet):
    """O'zbekiston viloyatlari (14 ta: 12 viloyat + Qoraqalpog'iston + Toshkent shahri)."""
    queryset = Viloyat.objects.all()
    serializer_class = ViloyatSerializer
    filterset_fields = ["turi"]
    search_fields = ["name_uz", "code"]
    lookup_field = "code"


class TumanViewSet(viewsets.ReadOnlyModelViewSet):
    """Tuman va viloyat bo'ysunuvidagi shaharlar. `?viloyat=<id>` bilan filtrlash mumkin."""
    queryset = Tuman.objects.select_related("viloyat").all()
    serializer_class = TumanSerializer
    filterset_fields = ["viloyat", "turi"]
    lookup_field = "slug"


class AholiPunktiViewSet(viewsets.ReadOnlyModelViewSet):
    """Qishloq/shaharchalar. `?tuman=<id>` bilan filtrlash mumkin."""
    queryset = AholiPunkti.objects.select_related("tuman", "tuman__viloyat").all()
    serializer_class = AholiPunktiSerializer
    filterset_fields = ["tuman"]
    lookup_field = "slug"


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    """Litsenziyaga ega tijorat banklari."""
    queryset = Bank.objects.select_related("viloyat").all()
    serializer_class = BankSerializer
    filterset_fields = ["turi", "viloyat"]
    lookup_field = "slug"


class OTMViewSet(viewsets.ReadOnlyModelViewSet):
    """Oliy ta'lim muassasalari (hozircha faqat davlat OTMlari)."""
    queryset = OTM.objects.select_related("viloyat").all()
    serializer_class = OTMSerializer
    filterset_fields = ["turi", "viloyat"]
    lookup_field = "slug"


class ValyutaViewSet(viewsets.ReadOnlyModelViewSet):
    """Valyutalar spravochnigi, har biri o'zining eng so'nggi kursi bilan."""
    queryset = Valyuta.objects.prefetch_related("kurslar").all()
    serializer_class = ValyutaSerializer
    lookup_field = "code"


class ValyutaKursiViewSet(viewsets.ReadOnlyModelViewSet):
    """Kunlik valyuta kurslari tarixi. `?valyuta=<id>&sana=YYYY-MM-DD` bilan filtrlash mumkin."""
    queryset = ValyutaKursi.objects.select_related("valyuta").all()
    serializer_class = ValyutaKursiSerializer
    filterset_fields = ["valyuta", "sana"]


class BayramViewSet(viewsets.ReadOnlyModelViewSet):
    """Bayramlar ta'rifi (nomi, turi, sanasi -- milliy bayramlar uchun)."""
    queryset = Bayram.objects.all()
    serializer_class = BayramSerializer
    filterset_fields = ["turi", "rasman_dam_olish_kuni"]
    lookup_field = "slug"


class BayramSanasiViewSet(viewsets.ReadOnlyModelViewSet):
    """Bayramlarning yilma-yil aniq sanalari. `?yil=2026` bilan filtrlash mumkin."""
    queryset = BayramSanasi.objects.select_related("bayram").all()
    serializer_class = BayramSanasiSerializer
    filterset_fields = ["yil", "bayram"]


class TelefonKodiViewSet(viewsets.ReadOnlyModelViewSet):
    """Mintaqaviy va mobil operator telefon kodlari."""
    queryset = TelefonKodi.objects.select_related("viloyat").all()
    serializer_class = TelefonKodiSerializer
    filterset_fields = ["turi", "viloyat"]


class NamozVaqtlariView(APIView):
    """
    Berilgan viloyat va sana uchun namoz vaqtlarini HISOBLAB beradi
    (bazadan o'qimaydi -- NOAA quyosh holati formulasi asosida real vaqtda
    hisoblanadi). Metodologiya va aniqlik chegaralari uchun
    geo/namoz_hisoblash.py'dagi docstringga qarang.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter("sana", str, description="YYYY-MM-DD (standart: bugun)"),
        ],
        responses=NamozVaqtlariSerializer,
    )
    def get(self, request, viloyat_code):
        viloyat = get_object_or_404(Viloyat, code=viloyat_code)
        if not viloyat.latitude or not viloyat.longitude:
            return Response({"xato": "Bu viloyat uchun koordinata kiritilmagan"}, status=422)

        sana_param = request.query_params.get("sana")
        sana = date_cls.fromisoformat(sana_param) if sana_param else date_cls.today()

        natija = namoz_vaqtlari(sana, float(viloyat.latitude), float(viloyat.longitude), tz_offset=5)
        data = {"viloyat": viloyat.name_uz, "sana": sana, **natija}
        return Response(NamozVaqtlariSerializer(data).data)
