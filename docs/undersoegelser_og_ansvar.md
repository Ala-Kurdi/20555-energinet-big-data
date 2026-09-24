1\. Er realtime-data lige anvendelige i vinter og sommer?



Jeg sammenlignede januar og juni og brugte kun komplette realtime-timer til beregningen af afvigelser.



Data viser, at realtime og afregningsdata ikke har samme afvigelsesmønster i de to perioder. For solproduktion var den gennemsnitlige absolutte forskel i januar 6,76 MWh i DK1 og 2,04 MWh i DK2. I juni var den 135,06 MWh i DK1 og 45,82 MWh i DK2.



Et konkret eksempel er 22. juni kl. 08:00 UTC i DK1. Her var realtime-solproduktionen 1459,07 MWh, mens afregningsdata viste 2758,33 MWh. Forskellen var derfor 1299,25 MWh. Timen havde alle 12 realtime-intervaller og havde ikke et kvalitetsflag i min pipeline.



Kvalitetsrapporten viste også 2 ufuldstændige time/prisområde-rækker i januar og 6 i juni.



Min observation er derfor, at realtime-data ikke opfører sig ens i januar og juni. Især soldata viser større forskelle i juni. Det betyder også, at en komplet time ikke nødvendigvis er det samme som en time, der ligger tæt på de senere afregningsdata.



Jeg kan dog ikke ud fra disse snapshots alene konkludere, at realtime-data generelt er dårligere om sommeren. Undersøgelsen dækker kun januar og juni 2026.





2\. Er forskellen mellem realtime og afregning den samme i DK1 og DK2?



Jeg sammenlignede DK1 og DK2 i januar og juni. Jeg brugte komplette realtime-timer og beregnede den gennemsnitlige absolutte forskel mellem realtime og afregningsdata.



Resultaterne viser, at forskellen ikke er den samme i DK1 og DK2. I januar var den gennemsnitlige forskel for onshore vind 108,03 MWh i DK1 og 11,33 MWh i DK2. I juni var forskellen for offshore vind 58,43 MWh i DK1 og 5,31 MWh i DK2. For sol i juni var forskellen 135,06 MWh i DK1 og 45,82 MWh i DK2.



Et konkret eksempel er 22. juni kl. 08:00 UTC. Her var forskellen mellem realtime og afregning for sol 1299,25 MWh i DK1, mens den var 294,69 MWh i DK2. Begge rækker havde alle 12 realtime-intervaller og ingen kvalitetsflag.



Min observation er, at realtime og afregningsdata i mine snapshots har større absolutte forskelle i DK1 end i DK2 for de tre undersøgte produktionstyper.



Data viser forskellen, men forklarer ikke alene, hvorfor DK1 og DK2 er forskellige. Derfor kan jeg ikke konkludere, at datakvaliteten generelt er dårligere i DK1 uden yderligere dokumentation eller metadata.





3\. Hvilke kvalitetsproblemer kan findes alene med regler, og hvilke kræver domæneviden eller metadata?



Nogle kvalitetsproblemer kan findes automatisk med simple regler i pipeline. Jeg kan for eksempel kontrollere, om en time har præcis 12 fem-minutters intervaller, om nøgler er duplikerede, om nødvendige kolonner findes, og om realtime og afregningsdata kan matches.



Kvalitetsrapporten viste 2 ufuldstændige time/prisområde-rækker i januar og 6 i juni. Der var ingen manglende joins i januar, juni eller DST-perioden.



Pipeline fandt også negative produktionsværdier. Der var 4 rækker med NEGATIVE\_PRODUCTION i januar, 37 i juni og 2 i DST-perioden. En regel kan finde de negative værdier, men reglen kan ikke alene afgøre, hvorfor værdierne er negative, eller om de er fejl.



Et konkret eksempel er DST-perioden. Her fandt pipeline negative produktionsværdier omkring skiftet til sommertid. Energinets metadata beskriver tekniske problemer og fejlagtige værdier omkring DST-skiftet. Her hjælper metadata derfor med at forstå et problem, som pipeline først har fundet med en regel.



Min konklusion er, at automatiske regler er gode til at finde mistænkelige data, men domæneviden og metadata er nødvendige for at forstå betydningen af nogle af problemerne. Derfor beholder jeg problemrækkerne og markerer dem med kvalitetsflag i stedet for automatisk at slette dem.





Big Data-vurdering



Energinet-casen kan forklares med flere Big Data-karakteristika.



Volume:

Realtime-data kommer hvert 5. minut og kan derfor hurtigt give mange rækker, når data gemmes over længere tid. I undervisningen arbejder jeg kun med snapshots fra januar, juni og DST-perioden, så mine filer er ikke i sig selv meget store. I et rigtigt system vil datamængden vokse løbende.



Velocity:

Realtime-data bliver produceret ofte, fordi der kommer nye målinger hvert 5. minut. Det stiller krav til, at data kan indlæses, valideres og behandles løbende. Afregningsdata kommer senere og har derfor en anden hastighed end realtime-data.



Variety:

Projektet bruger forskellige typer data. Realtime-data indeholder blandt andet 5-minutters målinger i MW, mens afregningsdata indeholder timeværdier i MWh. Dataene har derfor forskellig struktur, tidsopløsning og betydning, før de kan sammenlignes.



Veracity:

Datakvalitet er vigtig i denne case. Jeg fandt blandt andet ufuldstændige timer og negative produktionsværdier. Energinets metadata viser også, at realtime-data kan indeholde fejl. Derfor bruger pipeline kvalitetskontroller og kvalitetsflag i stedet for bare at stole på alle værdier.



Value:

Data får først rigtig værdi, når de bliver behandlet og kan bruges til analyse. I projektet omregner jeg MW til MWh, samler 5-minutters data til timer og sammenligner realtime med afregningsdata. Det gør det muligt at undersøge, hvor godt realtime-data kan bruges.



Samlet vurdering:

Mine snapshots er ikke alene “Big Data”, bare fordi de indeholder mange rækker. Big Data handler også om blandt andet hastighed, variation og datakvalitet. Casen viser derfor Big Data-problemer, som bliver vigtigere i et rigtigt system med løbende data over lang tid.





Platform, ansvar og sikkerhed



Jeg har sammenlignet tre mulige platforme til Energinet-casen: lokal Python/pandas, en delt PostgreSQL-database og en cloud-løsning som BigQuery.



Lokal Python/pandas:

Det er den løsning, jeg bruger i projektet. Den er enkel og passer godt til undervisning og mindre snapshots. Jeg kan køre hele pipeline lokalt og genskabe output fra raw-data. Ulempen er, at løsningen ikke er så god, hvis mange brugere skal arbejde med de samme data samtidig. Jeg har også selv ansvar for Python-miljø, filer, backup og adgang.



Delt PostgreSQL:

En PostgreSQL-database vil gøre det lettere for flere brugere og systemer at arbejde med de samme data. Data kan ligge centralt, og adgang kan styres med brugere og rettigheder. Til gengæld skal nogen have ansvar for drift, backup, opdateringer, sikkerhed og database-performance.



Cloud – BigQuery:

BigQuery er en cloud-baseret løsning, som kan bruges til store datamængder og analyse uden selv at drive databaseserveren. Det kan gøre skalering lettere. Cloud-platformen overtager dog ikke ansvaret for selve datakvaliteten. Virksomheden skal stadig styre adgang, definitioner, kvalitet og omkostninger.



Mit valg i denne case:

Til dette skoleprojekt er lokal Python/pandas tilstrækkeligt, fordi jeg arbejder med faste snapshots og selv kører analysen. Hvis løsningen skulle deles mellem flere brugere, ville en fælles database som PostgreSQL være mere relevant. Ved meget større datamængder og behov for skalering kunne en cloud-platform som BigQuery være relevant.



Ansvar og sikkerhed:

Uanset platform skal det være tydeligt, hvem der har ansvar for data, adgang, backup og ændringer. Brugere skal kun have den adgang, de har brug for. Raw-data bør bevares, så pipeline kan køres igen, og ændringer i kode og datadefinitioner bør dokumenteres og versioneres.



Energinet-dataene i denne case er data på prisområdeniveau og identificerer ikke i sig selv personer. Det betyder dog ikke, at alle energidata generelt er uden persondata. Hvis et andet system indeholder oplysninger om enkelte kunder eller husstande, skal persondata og adgang vurderes særskilt.





Antagelser og begrænsninger



Jeg arbejder med faste snapshots fra januar, juni og DST-perioden i 2026. Resultaterne kan derfor ikke automatisk bruges til at beskrive alle perioder eller hele Energinets datasæt.



Jeg bruger UTC som teknisk nøgle ved timeaggregation og join, mens dansk tid bevares til fortolkning.



En komplet realtime-time betyder i min pipeline, at der findes præcis 12 fem-minutters intervaller. Det betyder ikke automatisk, at værdierne er korrekte eller ligger tæt på afregningsdata.



Afregningsdata bruges som sammenligningsgrundlag, men betragtes ikke som et perfekt facit. Data kan blive opdateret senere.



Manglende værdier bliver ikke automatisk erstattet med nul, fordi en manglende værdi ikke nødvendigvis betyder nul.



Kvalitetsflag viser mistænkelige eller ufuldstændige data. Nogle problemer kan findes med regler, mens den endelige fortolkning kan kræve metadata eller domæneviden.

