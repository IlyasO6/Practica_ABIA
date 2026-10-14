# Optimització de rutes de distribució de combustible

Projecte en Python que utilitza cerca local per planificar el repartiment diari de combustible entre centres de distribució i gasolineres.

Desenvolupat per a l’assignatura Algorismes Bàsics per la Intel·ligència Artificial (ABIA) del Grau en Intel·ligència Artificial de la UPC, curs 2025–2026, primer quadrimestre.

El projecte compara Hill Climbing i Simulated Annealing i analitza com la representació de l’estat, els operadors, la inicialització i els paràmetres afecten la qualitat de les solucions i el temps d’execució.

## El problema

Una companyia de distribució ha de decidir quines peticions de combustible atén durant el dia, amb quin camió i mitjançant quins viatges.

Cada petició correspon a un dipòsit buit d’una gasolinera. Una mateixa gasolinera pot tenir diverses peticions pendents, amb diferents dies d’antiguitat.

L’objectiu és equilibrar:

- Els ingressos de les peticions ateses.
- El cost de transport.
- L’impacte de deixar peticions pendents.

### Restriccions del model base

| Paràmetre | Valor |
| --- | --- |
| Àrea geogràfica simulada | 100 × 100 km |
| Camions per centre | 1 |
| Capacitat per viatge | 2 dipòsits |
| Viatges màxims per camió i dia | 5 |
| Distància màxima per camió i dia | 640 km |
| Velocitat dels camions | 80 km/h |
| Jornada de treball | 8 hores |
| Valor base d’un dipòsit | 1.000 € |
| Cost de transport | 2 €/km |

Cada viatge comença i acaba al centre de distribució del camió. Pot servir una o dues peticions, de la mateixa gasolinera o de gasolineres diferents.

Els temps de càrrega i descàrrega es consideren instantanis.

### Distàncies i ingressos

Les distàncies es calculen amb la mètrica Manhattan:

```math
d(A,B)=|A_x-B_x|+|A_y-B_y|
```

L’ingrés d’una petició depèn dels dies que porta pendent:

```math
R(d)=
\begin{cases}
1000 \cdot 1.02, & d=0 \\
1000 \cdot \dfrac{100-2^d}{100}, & d\geq 1
\end{cases}
```

## Enfocament

El projecte modela el problema per utilitzar els algoritmes de cerca local proporcionats per les classes d’AIMA.

El desenvolupament inclou:

- La representació de les assignacions i les rutes.
- La construcció de solucions inicials vàlides.
- Els operadors de transformació.
- La generació de successors.
- La funció d’avaluació.
- L’experimentació i l’anàlisi dels resultats.

## Representació de l’estat

La classe `StateRepresentation`, descrita a `state.py`, manté les peticions assignades, els viatges dels camions i les magnituds necessàries per avaluar una solució:

- Benefici brut acumulat.
- Distància total recorreguda.
- Quilòmetres recorreguts per cada camió.
- Valor potencial de les peticions no assignades.

S’utilitzen matrius de distàncies per evitar repetir càlculs durant la cerca.

## Funció d’avaluació

La qualitat d’una solució es descriu mitjançant:

```math
Q(s)=B(s)-c_{\mathrm{km}}D(s)-0.5U(s)
```

On:

- `B(s)` és el benefici brut de les peticions ateses.
- `D(s)` és la distància total recorreguda.
- `c_km` és el cost per quilòmetre.
- `U(s)` és el valor potencial de les peticions no ateses, segons el model descrit a l’informe.

El pes `0.5` és una decisió del projecte per equilibrar la penalització de les peticions pendents amb els ingressos i el transport.

Una qualitat més alta és millor. Si la interfície de cerca requereix una heurística a minimitzar, la formulació equivalent és `h(s) = -Q(s)`.

El benefici net econòmic es calcula separadament:

```math
B_{\mathrm{net}}(s)=B(s)-c_{\mathrm{km}}D(s)
```

## Inicialització i operadors

S’han comparat tres estratègies de solució inicial:

| Estratègia | Descripció |
| --- | --- |
| Empty | Cap petició assignada. |
| Random | Assignació aleatòria respectant les restriccions. |
| Greedy | Construcció de rutes segons el benefici i la proximitat geogràfica. |

La inicialització seleccionada va ser greedy pel seu equilibri entre qualitat i temps d’execució.

El conjunt d’operadors seleccionat, `set_operadores_x`, permet assignar, eliminar i moure peticions, així com intercanviar-les dins d’un mateix camió.

## Experimentació

L’escenari de referència té 10 centres de distribució, 10 camions i 100 gasolineres.

L’estudi analitza:

1. La influència dels conjunts d’operadors.
2. L’efecte de la solució inicial.
3. L’ajust dels paràmetres de Simulated Annealing.
4. El temps d’execució en augmentar la mida del problema.
5. La reducció dels centres de distribució mantenint la flota.
6. L’augment del cost per quilòmetre.
7. La variació de la jornada de treball.

Els escenaris simulats es generen amb les classes proporcionades a `abia_Gasolina.py`. L’anàlisi estadística es documenta a `ExperimentacionEstadistica.rmd`.

La configuració de Simulated Annealing seleccionada a l’informe va ser `K = 50` i `Lambda = 0.0005`.

## Resultats

La comparació final presentada a l’informe va obtenir:

| Algoritme | Benefici brut (€) | Cost de transport (€) | Benefici net (€) | Temps (s) |
| --- | ---: | ---: | ---: | ---: |
| Hill Climbing | 96.734 | 5.512,4 | 91.222 | 10,89 |
| Simulated Annealing | 93.200 | 6.431,6 | 86.768,4 | 0,88 |

Els valors es reprodueixen amb els arrodoniments de l’informe.

En aquesta comparació, Hill Climbing va obtenir un benefici net superior, mentre que Simulated Annealing va requerir menys temps de càlcul.

Els resultats corresponen als escenaris i les configuracions estudiats; no impliquen que un algoritme sigui sempre superior a l’altre.

## Limitacions

- La cerca local no garanteix trobar l’òptim global.
- Els resultats depenen de la inicialització, els operadors i els paràmetres.
- Les dades són simulades, no provenen d’una xarxa logística real.
- El model simplifica el transport: no considera trànsit ni temps de càrrega i descàrrega.

## Autoria

- Laia Beyloc
- Ilyas Ouacham
- Nil Muriach

## Documentació

L’informe de la pràctica descriu les decisions de disseny, els experiments, l’anàlisi estadística i la comparació dels algoritmes.
