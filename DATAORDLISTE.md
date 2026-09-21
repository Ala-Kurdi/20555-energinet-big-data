# Dataordliste til Energinet-casen

## Grain

Grain beskriver, hvad én række repræsenterer.

- Realtime: ét femminuttersinterval i ét prisområde.
- Afregning: én time i ét prisområde.
- Dit endelige output: én UTC-time i ét prisområde.

Du kan ikke lave et fagligt forsvarligt join, før de to kilder har samme grain.

## Prisområde

Danmark er opdelt i `DK1` og `DK2`. En måling for DK1 må ikke uden videre sammenlignes med eller lægges oven i DK2. Prisområdet er en del af nøglen.

## Operationelle data

Data, der er tilgængelige hurtigt og bruges tæt på den løbende drift. De kan være foreløbige, estimerede, ufuldstændige eller ukorrigerede.

## Afregningsdata

Senere data, som er behandlet og modnet til afregning og statistik. De kan blive revideret over tid. Et enslydende kolonnenavn er ikke i sig selv bevis på samme forretningsdefinition.

## MW og MWh

- MW er effekt: hvor hurtigt energi produceres eller udveksles.
- MWh er energi over tid.

For et femminuttersinterval gælder:

```text
MWh = MW × 5/60
```

Omregn hvert interval og summér derefter til timer.

## UTC og dansk tid

UTC er stabil som teknisk tidsnøgle. Dansk tid er nødvendig, når mennesker skal fortolke datoer og klokkeslæt. Ved skiftet til sommertid kan et lokalt døgn have 23 timer.

## Primær nøgle

Den kombination af kolonner, som entydigt identificerer en række:

- realtime: `(Minutes5UTC, PriceArea)`;
- afregning: `(HourUTC, PriceArea)`;
- analyseoutput: `(hour_utc, price_area)`.

## Storebælt

Storebæltsforbindelsen flytter energi mellem DK1 og DK2. Den er derfor:

- ikke udenlandsk udveksling for Danmark;
- relevant for balancen i hvert af de to prisområder.

## Strukturel null-værdi

En tom værdi kan betyde, at en forbindelse ikke findes i det pågældende prisområde. Det er noget andet end en ukendt måling. Du skal undersøge kolonnen og dokumentere, hvorfor en null eventuelt behandles som nul.

## Kvalitetsflag

En kolonne, der fortæller, om en række kræver særlig opmærksomhed. Flag gør det muligt at bevare data og samtidig være tydelig om problemer.

Eksempler:

- ufuldstændig realtime-time;
- række findes kun i én kilde;
- negativ produktionsværdi;
- mistænkeligt uændrede værdier;
- kendt fejl omtalt i metadata.

## WAPE

Weighted Absolute Percentage Error sammenfatter den samlede absolutte afvigelse i forhold til den samlede størrelse af referenceværdierne:

```text
WAPE = sum(abs(realtime - afregning)) / sum(abs(afregning)) × 100
```

WAPE er valgfri i minimumsløsningen. Et fejlmål erstatter ikke undersøgelse af enkelte timer, definitioner og datakvalitet.
