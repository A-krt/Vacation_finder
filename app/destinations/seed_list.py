from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DestinationSeed:
    city: str
    country: str
    arrival_airport: str
    fit_score: float = 0.0

DESTINATIONS = [
    DestinationSeed(city="Alicante", country="Spain", arrival_airport="ALC"),
    DestinationSeed(city="Valencia", country="Spain", arrival_airport="VLC"),
    DestinationSeed(city="Malaga", country="Spain", arrival_airport="AGP"),
    DestinationSeed(city="Palma de Mallorca", country="Spain", arrival_airport="PMI"),
    DestinationSeed(city="Ibiza", country="Spain", arrival_airport="IBZ"),
    DestinationSeed(city="Menorca", country="Spain", arrival_airport="MAH"),
    DestinationSeed(city="Lanzarote", country="Spain", arrival_airport="ACE"),
    DestinationSeed(city="Fuerteventura", country="Spain", arrival_airport="FUE"),
    DestinationSeed(city="Gran Canaria", country="Spain", arrival_airport="LPA"),
    DestinationSeed(city="Tenerife South", country="Spain", arrival_airport="TFS"),
    DestinationSeed(city="Barcelona", country="Spain", arrival_airport="BCN"),
    DestinationSeed(city="Seville", country="Spain", arrival_airport="SVQ"),
    DestinationSeed(city="Bilbao", country="Spain", arrival_airport="BIO"),
    DestinationSeed(city="Murcia", country="Spain", arrival_airport="RMU"),
    DestinationSeed(city="Jerez de la Frontera", country="Spain", arrival_airport="XRY"),
    DestinationSeed(city="Almeria", country="Spain", arrival_airport="LEI"),
    DestinationSeed(city="Girona", country="Spain", arrival_airport="GRO"),
    DestinationSeed(city="Reus", country="Spain", arrival_airport="REU"),
    DestinationSeed(city="Santiago de Compostela", country="Spain", arrival_airport="SCQ"),
    DestinationSeed(city="Asturias", country="Spain", arrival_airport="OVD"),

    DestinationSeed(city="Faro", country="Portugal", arrival_airport="FAO"),
    DestinationSeed(city="Lisbon", country="Portugal", arrival_airport="LIS"),
    DestinationSeed(city="Porto", country="Portugal", arrival_airport="OPO"),
    DestinationSeed(city="Madeira", country="Portugal", arrival_airport="FNC"),
    DestinationSeed(city="Ponta Delgada", country="Portugal", arrival_airport="PDL"),
    DestinationSeed(city="Porto Santo", country="Portugal", arrival_airport="PXO"),

    DestinationSeed(city="Antalya", country="Turkey", arrival_airport="AYT"),
    DestinationSeed(city="Dalaman", country="Turkey", arrival_airport="DLM"),
    DestinationSeed(city="Bodrum", country="Turkey", arrival_airport="BJV"),
    DestinationSeed(city="Izmir", country="Turkey", arrival_airport="ADB"),
    DestinationSeed(city="Istanbul", country="Turkey", arrival_airport="IST"),
    DestinationSeed(city="Gazipasa-Alanya", country="Turkey", arrival_airport="GZP"),

    DestinationSeed(city="Heraklion", country="Greece", arrival_airport="HER"),
    DestinationSeed(city="Chania", country="Greece", arrival_airport="CHQ"),
    DestinationSeed(city="Rhodes", country="Greece", arrival_airport="RHO"),
    DestinationSeed(city="Kos", country="Greece", arrival_airport="KGS"),
    DestinationSeed(city="Corfu", country="Greece", arrival_airport="CFU"),
    DestinationSeed(city="Zakynthos", country="Greece", arrival_airport="ZTH"),
    DestinationSeed(city="Santorini", country="Greece", arrival_airport="JTR"),
    DestinationSeed(city="Mykonos", country="Greece", arrival_airport="JMK"),
    DestinationSeed(city="Thessaloniki", country="Greece", arrival_airport="SKG"),
    DestinationSeed(city="Athens", country="Greece", arrival_airport="ATH"),
    DestinationSeed(city="Kefalonia", country="Greece", arrival_airport="EFL"),
    DestinationSeed(city="Skiathos", country="Greece", arrival_airport="JSI"),

    DestinationSeed(city="Larnaca", country="Cyprus", arrival_airport="LCA"),
    DestinationSeed(city="Paphos", country="Cyprus", arrival_airport="PFO"),

    DestinationSeed(city="Catania", country="Italy", arrival_airport="CTA"),
    DestinationSeed(city="Palermo", country="Italy", arrival_airport="PMO"),
    DestinationSeed(city="Naples", country="Italy", arrival_airport="NAP"),
    DestinationSeed(city="Bari", country="Italy", arrival_airport="BRI"),
    DestinationSeed(city="Brindisi", country="Italy", arrival_airport="BDS"),
    DestinationSeed(city="Cagliari", country="Italy", arrival_airport="CAG"),
    DestinationSeed(city="Olbia", country="Italy", arrival_airport="OLB"),
    DestinationSeed(city="Lamezia Terme", country="Italy", arrival_airport="SUF"),
    DestinationSeed(city="Pisa", country="Italy", arrival_airport="PSA"),
    DestinationSeed(city="Rome", country="Italy", arrival_airport="FCO"),
    DestinationSeed(city="Venice", country="Italy", arrival_airport="VCE"),
    DestinationSeed(city="Milan Malpensa", country="Italy", arrival_airport="MXP"),
    DestinationSeed(city="Alghero", country="Italy", arrival_airport="AHO"),
    DestinationSeed(city="Trapani", country="Italy", arrival_airport="TPS"),

    DestinationSeed(city="Dubrovnik", country="Croatia", arrival_airport="DBV"),
    DestinationSeed(city="Split", country="Croatia", arrival_airport="SPU"),
    DestinationSeed(city="Zadar", country="Croatia", arrival_airport="ZAD"),
    DestinationSeed(city="Pula", country="Croatia", arrival_airport="PUY"),
    DestinationSeed(city="Rijeka", country="Croatia", arrival_airport="RJK"),

    DestinationSeed(city="Malta", country="Malta", arrival_airport="MLA"),

    DestinationSeed(city="Nice", country="France", arrival_airport="NCE"),
    DestinationSeed(city="Marseille", country="France", arrival_airport="MRS"),
    DestinationSeed(city="Montpellier", country="France", arrival_airport="MPL"),
    DestinationSeed(city="Toulouse", country="France", arrival_airport="TLS"),
    DestinationSeed(city="Bordeaux", country="France", arrival_airport="BOD"),
    DestinationSeed(city="Ajaccio", country="France", arrival_airport="AJA"),
    DestinationSeed(city="Bastia", country="France", arrival_airport="BIA"),

    DestinationSeed(city="Tirana", country="Albania", arrival_airport="TIA"),
    DestinationSeed(city="Podgorica", country="Montenegro", arrival_airport="TGD"),
    DestinationSeed(city="Tivat", country="Montenegro", arrival_airport="TIV"),

    DestinationSeed(city="Varna", country="Bulgaria", arrival_airport="VAR"),
    DestinationSeed(city="Burgas", country="Bulgaria", arrival_airport="BOJ"),
    DestinationSeed(city="Sofia", country="Bulgaria", arrival_airport="SOF"),

    DestinationSeed(city="Marrakech", country="Morocco", arrival_airport="RAK"),
    DestinationSeed(city="Agadir", country="Morocco", arrival_airport="AGA"),
    DestinationSeed(city="Casablanca", country="Morocco", arrival_airport="CMN"),
    DestinationSeed(city="Tangier", country="Morocco", arrival_airport="TNG"),
    DestinationSeed(city="Fez", country="Morocco", arrival_airport="FEZ"),

    DestinationSeed(city="Hurghada", country="Egypt", arrival_airport="HRG"),
    DestinationSeed(city="Sharm El Sheikh", country="Egypt", arrival_airport="SSH"),

    DestinationSeed(city="Tunis", country="Tunisia", arrival_airport="TUN"),
    DestinationSeed(city="Djerba", country="Tunisia", arrival_airport="DJE"),
    DestinationSeed(city="Monastir", country="Tunisia", arrival_airport="MIR"),

    DestinationSeed(city="Vienna", country="Austria", arrival_airport="VIE"),
    DestinationSeed(city="Salzburg", country="Austria", arrival_airport="SZG"),
    DestinationSeed(city="Geneva", country="Switzerland", arrival_airport="GVA"),
    DestinationSeed(city="Zurich", country="Switzerland", arrival_airport="ZRH"),

    DestinationSeed(city="Prague", country="Czechia", arrival_airport="PRG"),
    DestinationSeed(city="Budapest", country="Hungary", arrival_airport="BUD"),
    DestinationSeed(city="Bucharest", country="Romania", arrival_airport="OTP"),
    DestinationSeed(city="Belgrade", country="Serbia", arrival_airport="BEG"),
    DestinationSeed(city="Skopje", country="North Macedonia", arrival_airport="SKP"),

    DestinationSeed(city="Krakow", country="Poland", arrival_airport="KRK"),
    DestinationSeed(city="Ljubljana", country="Slovenia", arrival_airport="LJU"),
]
