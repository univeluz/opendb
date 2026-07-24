from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("viloyatlar", views.ViloyatViewSet, basename="viloyat")
router.register("tumanlar", views.TumanViewSet, basename="tuman")
router.register("aholi-punktlari", views.AholiPunktiViewSet, basename="aholipunkti")
router.register("banklar", views.BankViewSet, basename="bank")
router.register("otmlar", views.OTMViewSet, basename="otm")
router.register("valyutalar", views.ValyutaViewSet, basename="valyuta")
router.register("valyuta-kurslari", views.ValyutaKursiViewSet, basename="valyutakursi")
router.register("bayramlar", views.BayramViewSet, basename="bayram")
router.register("bayram-sanalari", views.BayramSanasiViewSet, basename="bayramsanasi")
router.register("telefon-kodlari", views.TelefonKodiViewSet, basename="telefonkodi")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "namoz-vaqtlari/<str:viloyat_code>/",
        views.NamozVaqtlariView.as_view(),
        name="namoz-vaqtlari",
    ),
]
