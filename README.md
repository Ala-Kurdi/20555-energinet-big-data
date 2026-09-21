# 20555 – Starterprojekt: Kan vi stole på live-eldata?

## Din opgave

Du skal bygge en reproducerbar datapipeline, som sammenligner Energinets operationelle femminuttersdata med senere afregningsdata.

```text
rå JSON
→ validering
→ MW til MWh
→ timeaggregation
→ join
→ kvalitetsflag
→ analyseklart output
→ undersøgelse og faglig forklaring
```

Du skal ikke have API-adgang. Projektet indeholder faste danske datasnapshots, så alle kan arbejde på samme datagrundlag og fortsætte uden internet.

## Start her

1. Åbn en terminal i denne mappe.
2. Kontrollér setup og data:

```powershell
python check_setup.py
```

3. Læs [OPGAVE.md](OPGAVE.md) og [DATAORDLISTE.md](DATAORDLISTE.md).
4. Åbn `src/pipeline.py`, og begynd ved `TODO 1`.
5. Brug først den lille periode omkring sommertidsskiftet:

```powershell
python run_pipeline.py --period dst
```

Det er forventet, at den sidste kommando stopper ved en `TODO`, før du har implementeret pipelinen.

## Krav til software

- Python 3.11 eller nyere
- `pandas`

Installer projektets bibliotek, hvis det ikke allerede findes:

```powershell
python -m pip install -r requirements.txt
```

## Projektets vigtigste filer

| Fil eller mappe | Hvad bruger du den til? |
|---|---|
| `OPGAVE.md` | Dagsplan, krav, spørgsmål og afleveringsbevis |
| `DATAORDLISTE.md` | Centrale data- og domænebegreber |
| `data/raw/` | Uændrede snapshots fra Energinet |
| `data/snapshot_manifest.json` | Filstørrelser, rækkeantal og checksums |
| `src/contracts.py` | Kolonner og navne, som din løsning skal kende |
| `src/pipeline.py` | Dit kode-skelet med nummererede TODO'er |
| `run_pipeline.py` | Kører din pipeline for en valgt periode |
| `output/` | Her skriver du dine egne mellem- og slutfiler |

## Vigtige spilleregler

- Redigér ikke filer i `data/raw/`.
- Bevar rådata og afledte data i forskellige mapper.
- En række må ikke forsvinde lydløst. Flag eller dokumentér fravalg.
- Brug UTC som teknisk joinnøgle, og bevar dansk tid til fortolkning.
- Beskriv afregningsdata som senere og mere modnede data—ikke automatisk som den eneste sandhed.
- Brug ikke underviserens referenceimplementation som startkode.

## Hjælp til fejlsøgning

- Hvis `check_setup.py` fejler på en checksum, skal du hente en ny kopi af starterprojektets data hos underviseren.
- Hvis Python ikke kan finde `pandas`, skal du installere `requirements.txt` eller vælge skolens Python-miljø.
- Hvis pipelinen stopper med `NÆSTE TODO`, er setup i orden; fortsæt i `src/pipeline.py`.
