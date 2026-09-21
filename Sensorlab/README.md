# Sensorlab – separate miniopgaver til 20555

> **Status:** ARBEJDSDOKUMENT  
> **Data:** Konstruerede undervisningseksempler, ikke virkelige målinger

## Start

Kopiér hele Sensorlab-mappen til dit eget arbejdsområde. Den kræver Python 3.11+ og pandas. Installér før offlineundervisning:

```powershell
python -m pip install -r requirements.txt
python demo_read.py
```

Kør derefter `python exercises.py`, når Modul02 begynder. Den stopper ved en navngivet miniopgave, indtil du har implementeret den.

## Data og betydning

`flow.json` indeholder middelvandflow i liter/minut over 10 minutter fra tidspunktet i UTC. A og B har seks tidspositioner hver; en manglende måling betyder ukendt, ikke nul. `manual.csv` er en separat manuel opgørelse i liter pr. UTC-time og enhed. Den er en sammenligningskilde, ikke automatisk sandhed. C findes kun i den manuelle opgørelse.

`devices.csv` er enhedsregister. `device.xml` beskriver én enhed. `service.txt` er en ustruktureret servicetekst. `plan.json` beskriver dependencies; den udfører ikke kode.

## Arbejdsform

Følg `20555_Laerling_Miniopgaver_ModulNN.md` for det aktuelle modul. Skriv korte svar i din egen notesfil og kode i en kopi af `exercises.py`. Miniopgaverne samles op i undervisningen. De er ikke fem ekstra projektafleveringer.

Kodeeksemplerne træner principper. Energinet har andre nøgler, tidsintervaller, enheder og domæneregler; overførslen er dit selvstændige arbejde.
