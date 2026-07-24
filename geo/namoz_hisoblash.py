"""
Namoz vaqtlarini hisoblash -- NOAA quyosh holati algoritmi asosida.

METODOLOGIYA:
- Quyosh deklinatsiyasi va vaqt tenglamasi: NOAA Solar Calculator formulasi
  (https://gml.noaa.gov/grad/solcalc/) -- foydalanuvchi avval xuddi shu
  yondashuvni faqat Shom (Maghrib) uchun ishlatgan, bu yerda barcha 6 vaqtga
  kengaytirildi.
- Asr: Hanafiy uslub (soya koeffitsiyenti = 2) -- O'zbekistonda amaliyotda
  qo'llaniladigan standart (namoz-vaqti.com kabi bir nechta mustaqil manba
  tomonidan tasdiqlangan).
- Fajr/Isha burchagi: 15°/15° -- BU ANIQ HUJJATLASHTIRILGAN MANBADAN OLINGAN
  EMAS. Global standartlarda odatda 18°/17° (Jahon Musulmonlar Ligasi)
  ishlatiladi, lekin bu qiymat namozvaqti.uz'ning haqiqiy e'lon qilingan
  jadvaliga (manbasi: "Book Media Nashr" 2024-2025 taqvim kitobi) EMPIRIK
  ravishda ikkita mavsumda (24-iyul va 15-yanvar 2026, Toshkent) mos
  kelishi orqali aniqlandi -- pastdagi VALIDATSIYA bo'limiga qarang.

VALIDATSIYA (Toshkent, lat=41.2995, lon=69.2401, tz=+5):
                  24-iyul-2026          15-yanvar-2026
  Vaqt      Hisob.   Haqiqiy   Farq   Hisob.   Haqiqiy   Farq
  Bomdod    03:37    03:34     +3d    06:26    06:23     +3d
  Quyosh    05:10    05:11     -1d    07:47    07:47      0
  Peshin    12:31    12:34     -3d    12:33    12:37     -4d
  Asr       17:37    17:36     +1d    15:37    15:37      0
  Shom      19:49    19:50     -1d    17:18    17:20     -2d
  Xufton    21:22    21:21     +1d    18:39    18:39      0

Xulosa: eng katta farq 4 daqiqa (Peshin), aksariyati 0-2 daqiqa. Bu farqlar
ehtimol nashriyot tomonidan qo'llangan kichik "ehtiyot" marjasi (masalan
Peshin va Shomni bir necha daqiqa kechroq, Bomdodni bir necha daqiqa
ertaroq e'lon qilish -- keng tarqalgan amaliyot). PRECISION_NOTE: bu modul
"toza" astronomik vaqtni beradi (ehtiyotsiz); agar mahalliy nashr bilan
farqlarni yanada kamaytirmoqchi bo'lsang, quyidagi EHTIYOT_DAQIQA lug'atini
qo'llash mumkin (ixtiyoriy, standart o'chirilgan).
"""
import math
from datetime import date


# Ixtiyoriy -- namozvaqti.uz bilan yaqinroq moslashtirish uchun (standart: qo'llanilmaydi)
EHTIYOT_DAQIQA = {"bomdod": -3, "peshin": +3, "asr": 0, "shom": +2, "xufton": 0}


def julian_day(d: date) -> float:
    y, m, day = d.year, d.month, d.day
    if m <= 2:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + A // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + day + B - 1524.5


def solar_declination_and_eqtime(jd: float):
    """NOAA formulasi. Qaytaradi: (deklinatsiya gradusda, vaqt tenglamasi daqiqada)."""
    T = (jd - 2451545.0) / 36525.0
    L0 = (280.46646 + T * (36000.76983 + T * 0.0003032)) % 360
    M = 357.52911 + T * (35999.05029 - 0.0001537 * T)
    Mrad = math.radians(M)
    e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T)
    C = (math.sin(Mrad) * (1.914602 - T * (0.004817 + 0.000014 * T))
         + math.sin(2 * Mrad) * (0.019993 - 0.000101 * T)
         + math.sin(3 * Mrad) * 0.000289)
    true_long = L0 + C
    omega = 125.04 - 1934.136 * T
    lambda_ = true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))
    seconds = 21.448 - T * (46.8150 + T * (0.00059 - T * 0.001813))
    e0 = 23.0 + (26.0 + seconds / 60.0) / 60.0
    epsilon = e0 + 0.00256 * math.cos(math.radians(omega))

    delta = math.degrees(math.asin(
        math.sin(math.radians(epsilon)) * math.sin(math.radians(lambda_))
    ))
    y = math.tan(math.radians(epsilon) / 2) ** 2
    EqT = 4 * math.degrees(
        y * math.sin(2 * math.radians(L0))
        - 2 * e * math.sin(Mrad)
        + 4 * e * y * math.sin(Mrad) * math.cos(2 * math.radians(L0))
        - 0.5 * y * y * math.sin(4 * math.radians(L0))
        - 1.25 * e * e * math.sin(2 * Mrad)
    )
    return delta, EqT


def _hour_angle_for_depression(lat_deg, delta_deg, angle_below_horizon_deg):
    lat, delta = math.radians(lat_deg), math.radians(delta_deg)
    cos_h = (-math.sin(math.radians(angle_below_horizon_deg)) - math.sin(lat) * math.sin(delta)) / (
        math.cos(lat) * math.cos(delta)
    )
    cos_h = max(-1.0, min(1.0, cos_h))
    return math.degrees(math.acos(cos_h))


def _asr_hour_angle(lat_deg, delta_deg, shadow_factor):
    lat, delta = math.radians(lat_deg), math.radians(delta_deg)
    altitude = math.degrees(math.atan(1.0 / (shadow_factor + math.tan(abs(lat - delta)))))
    cos_h = (math.sin(math.radians(altitude)) - math.sin(lat) * math.sin(delta)) / (
        math.cos(lat) * math.cos(delta)
    )
    cos_h = max(-1.0, min(1.0, cos_h))
    return math.degrees(math.acos(cos_h))


def _hours_to_hhmm(hours):
    hours = hours % 24
    h = int(hours)
    m = int(round((hours - h) * 60))
    if m == 60:
        m, h = 0, (h + 1) % 24
    return f"{h:02d}:{m:02d}"


def namoz_vaqtlari(d: date, lat: float, lon: float, tz_offset: float,
                    fajr_angle=15.0, isha_angle=15.0, asr_factor=2,
                    ehtiyot=False):
    """
    Berilgan sana/joylashuv uchun 6 ta namoz vaqtini hisoblaydi.

    lat, lon: gradusda (Uzbekiston uchun lon musbat, sharq)
    tz_offset: soat mintaqasi UTC'dan farqi (O'zbekiston uchun doim +5)
    asr_factor: 1=Shofeiy/boshqa mazhablar, 2=Hanafiy (standart, O'zbekiston uchun)
    ehtiyot: True bo'lsa EHTIYOT_DAQIQA qo'llanadi (namozvaqti.uz'ga yanada yaqinroq)
    """
    jd = julian_day(d)
    delta, eqt = solar_declination_and_eqtime(jd)
    solar_noon = 12.0 - lon / 15.0 - eqt / 60.0 + tz_offset

    h_sunrise = _hour_angle_for_depression(lat, delta, 0.833)
    h_fajr = _hour_angle_for_depression(lat, delta, fajr_angle)
    h_isha = _hour_angle_for_depression(lat, delta, isha_angle)
    h_asr = _asr_hour_angle(lat, delta, asr_factor)

    raw = {
        "bomdod": solar_noon - h_fajr / 15.0,
        "quyosh": solar_noon - h_sunrise / 15.0,
        "peshin": solar_noon,
        "asr": solar_noon + h_asr / 15.0,
        "shom": solar_noon + h_sunrise / 15.0,
        "xufton": solar_noon + h_isha / 15.0,
    }
    if ehtiyot:
        for k, mins in EHTIYOT_DAQIQA.items():
            raw[k] += mins / 60.0

    return {k: _hours_to_hhmm(v) for k, v in raw.items()}
