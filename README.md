# Vacation_finder

Een Python-project dat vakantiedeals zoekt op basis van de regels:

- vertrek vanaf AMS
- 2 volwassenen
- juli en augustus 2026
- 9 t/m 11 nachten
- directe retourvluchten
- 1 gedeelde grote koffer
- verblijf met eigen badkamer + tweepersoonsbed
- kwaliteit: 4-sterrenhotel **of** review >= 4.0/5 **of** review >= 8.0/10
- totaalbudget maximaal €1.500
- ranking op beste prijs-kwaliteit
- output in terminal en CSV

## Status
Deze eerste versie gebruikt **mock adapters** voor vluchten, verblijf en transfers.
De business-logica, filters, ranking en export zijn al volledig opgezet.
Later kun je de mock adapters vervangen door echte API- of scraping-adapters.

## Lokaal draaien
```bash
python run.py
