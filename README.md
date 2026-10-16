# 🎮 Nordlysjeger

Et arkadespill laget i Python med Pygame. Du styrer en lysende ånd som
svever over en nattlig fjord, samler nordlys-partikler og unngår fallende
iskrystaller. Vanskelighetsgraden øker automatisk over tid.

## Hvordan kjøre spillet

1. Installer Python 3.10 eller nyere.
2. Åpne en terminal i prosjektmappen.
3. Installer avhengigheter:

4. Start spillet:

## Kontroller

| Tast             | Handling         |
| ---------------- | ---------------- |
| Piltaster / WASD | Beveg spilleren  |
| P eller ESC      | Pause / fortsett |
| ENTER / SPACE    | Start / restart  |
| Q (i pause)      | Tilbake til meny |
| ESC (i meny)     | Avslutt spillet  |

## Mål

Få høyest mulig poengsum før du mister alle 3 livene. Rekorden din lagres
automatisk i `highscore.txt`.

## Mappestruktur

- `main.py` – startfil
- `src/` – all spillkode
- `docs/` – planlegging, dokumentasjon og egenvurdering

## Teknologi

- Python 3.10+
- Pygame 2.6

# 1. Planlegging

## Idé

**Nordlysjeger** er et enkelt, men stemningsfullt arkadespill inspirert av
nordnorsk natur. Spilleren styrer en lysende ånd som svever gjennom en
nattlig fjordlandskap, samler glødende nordlys-partikler og unngår
fallende iskrystaller. Spillet er lett å lære, men blir gradvis vanskeligere.

## Målgruppe

Barn og unge (10–18 år) og andre som liker korte, koselige arkadespill.
Spillet krever ingen forkunnskaper og kan spilles i korte økter på 1–3 minutter.

## Mål i spillet

- Samle så mange nordlys-partikler som mulig før du mister alle livene.
- Overlev så lenge som mulig – vanskelighetsgraden øker for hvert 20. sekund.

## Planlagte mekanikker

| Mekanikk                      | Beskrivelse                                   |
| ----------------------------- | --------------------------------------------- |
| Poengsystem                   | +10 poeng per nordlys-partikkel               |
| Liv / helse                   | 3 liv, -1 per kollisjon med iskrystall        |
| Nivåer                        | Nivå øker automatisk, farten på objekter øker |
| Bevegelige objekter           | Nordlys og iskrystaller faller nedover        |
| Kollisjoner                   | Rektangelbasert kollisjonssjekk               |
| Startmeny / pause / game over | Tre separate spilltilstander                  |
| Highscore                     | Lagres til fil og lastes ved oppstart         |

## Design og visuell stil

- Mørk natt med gradient fra dyp blå til lilla
- Stjerner som prikker i bakgrunnen
- Nordlys-partikler gløder i grønt, lilla eller blått
- Iskrystaller er roterende, lyseblå diamanter
- Spilleren er en glødende hvit/grønn sirkel
- Enkel, lesbar HUD øverst på skjermen

## Verktøyvalg

- **Python 3.10+** – kjent språk, godt egnet for 2D-spill.
- **Pygame 2.6** – enkelt bibliotek for grafikk, input og lyd.
- **VS Code** – editor med Python-utvidelse og integrert terminal.
- **Git + GitHub** – versjonskontroll og innlevering.

## Fremdriftsplan (3 økter)

- **Økt 1:** Idé, planlegging, prosjektoppsett i VS Code, tomt vindu med Pygame.
- **Økt 2:** Plan godkjennes → spiller, objekter, kollisjoner, HUD, menyer.
- **Økt 3:** Testing, justering av vanskelighetsgrad, dokumentasjon, innlevering.

# 2. Utviklingsprosess

## Oppsett

Prosjektet ble satt opp i VS Code med følgende struktur:

- `main.py` som startpunkt
- `src/`-pakke for all logikk
- `docs/` for dokumentasjon

Jeg valgte en modulær struktur fordi det gjør koden lettere å lese,
teste og utvide. Hver klasse har ett tydelig ansvar:

| Fil           | Ansvar                                      |
| ------------- | ------------------------------------------- |
| `settings.py` | Alle konstanter på ett sted                 |
| `player.py`   | Spillerens posisjon, input og tegning       |
| `objects.py`  | Nordlys og iskrystaller                     |
| `game.py`     | Spilltilstander, spawn-logikk, HUD, tegning |

## Iterativ utvikling

Jeg utviklet spillet i små steg og testet etter hvert steg:

1. **Vindu + spill-loop** – fikk et svart vindu med jevn FPS.
2. **Spiller** – kunne bevege en sirkel med piltastene.
3. **Fallende objekter** – nordlys og iskrystaller spawnet og falt nedover.
4. **Kollisjoner** – `pygame.Rect.colliderect` ga poeng og tap av liv.
5. **HUD** – viste poeng, nivå, liv og rekord.
6. **Menyer** – start-, pause- og game over-skjermer.
7. **Highscore** – lagret til `highscore.txt`.
8. **Polering** – glød-effekter, gradient-bakgrunn, stjerner, nivåøkning.

## Utfordringer og løsninger

### Utfordring 1: Bevegelse føltes "hakkete" diagonalt

Når spilleren beveget seg diagonalt, gikk den fortere enn horisontalt/vertikalt
fordi vektoren (1, 1) har lengde √2 ≈ 1.41.
**Løsning:** Normaliserte vektoren ved å multiplisere begge komponentene med
1/√2 ≈ 0.7071 når begge er ulik null.

### Utfordring 2: Objekter bygget seg opp på skjermen

Tidligere objekter ble ikke fjernet når de forlot skjermen.
**Løsning:** Itererte over en kopi av listen (`self.particles[:]`) og fjernet
objekter med `off_screen()`. Måtte iterere over en kopi for å unngå at
indekser ble forskjøvet mens jeg fjernet elementer.

### Utfordring 3: Bakgrunnen var treg å tegne

Å tegne gradient-linjer hver frame brukte mye CPU.
**Løsning:** Forhåndsrenderte bakgrunnen én gang til en `Surface` og blit-er
den hver frame. Dette er et standard Pygame-optimaliseringstriks.

### Utfordring 4: Kollisjon traff for tidlig / for sent

Rektanglene til sirkelobjektene var litt større enn selve sirkelen.
**Løsning:** Brukte `radius * 2` som bredde/høyde og oppdaterte
`rect.center` etter hver posisjonsendring.

## Testing

Jeg testet spillet etter hver endring. Testpunkter:

- Beveger spilleren seg jevnt i alle retninger?
- Blir spilleren innenfor skjermen?
- Forsvinner objekter når de treffer bunnen?
- Fungerer kollisjoner korrekt (poeng og tap av liv)?
- Starter, pauser og restarter spillet som forventet?
- Lagres rekorden når man dør?

## Hva jeg lærte

- Å strukturere et prosjekt i moduler gir bedre oversikt.
- Klasser med ett ansvar er lettere å feilsøke.
- Små, hyppige tester sparer tid i lengden.
- Pygame er enkelt å komme i gang med, men ytelse krever omtanke
  (f.eks. forhåndsrendering av bakgrunn).

# 3. Bruk av KI

## Hva jeg brukte KI til

Jeg brukte KI som en **sparringspartner og feilsøker**, ikke som
kodegenerator. All kode er skrevet og forstått av meg. KI ble brukt til:

1. Å forklare Pygame-funksjoner jeg ikke kjente (f.eks. `SRCALPHA`,
   `Surface.blit`, `pygame.Rect.colliderect`).
2. Å finne årsaken til bugs.
3. Å gi forslag til forbedringer (glød-effekt, gradient-bakgrunn).
4. Å lage en realistisk fremdriftsplan.

## Konkrete eksempler

### Eksempel 1 – Diagonal-bevegelse

**Problem:** Spilleren gikk fortere diagonalt enn horisontalt.
**Prompt:**

> "I Pygame, spilleren min beveger seg fortere når jeg trykker to piltaster
> samtidig. Hvordan kan jeg normalisere bevegelsen uten å bruke vektorer?"

**Svar (oppsummert):** Multipliser begge retninger med 1/√2 ≈ 0.7071 når
begge er ulik null.
**Hvordan jeg brukte det:** La inn sjekken `if dx != 0 and dy != 0` i
`Player.update`. Testet – bevegelsen ble jevn. Forsto hvorfor: lengden
på (1,1) er √2, og vi vil at lengden alltid skal være 1.

### Eksempel 2 – Objekter forsvant ikke

**Problem:** Nordlys og iskrystaller samlet seg i bunnen av skjermen.
**Prompt:**

> "Hvorfor blir elementene i listen min liggende selv om jeg kaller
> `remove()` på dem i en for-løkke?"

**Svar (oppsummert):** Når du fjerner elementer fra en liste mens du itererer
over den, hopper løkken over elementer fordi indeksene forskyves. Iterer
over en **kopi** (`liste[:]`).
**Hvordan jeg brukte det:** Endret alle oppdateringsløkker til å iterere over
`self.particles[:]` og `self.shards[:]`. Fungerte umiddelbart.

### Eksempel 3 – Glød-effekt

**Problem:** Spilleren så flat og kjedelig ut.
**Prompt:**

> "Hvordan kan jeg lage en glødeeffekt rundt en sirkel i Pygame uten å
> bruke bilder?"

**Svar (oppsummert):** Lag en `Surface` med `SRCALPHA`, tegn flere
konsentriske sirkler med lav alpha, og blit den over skjermen.
**Hvordan jeg brukte det:** Implementerte gløden på spilleren og
nordlys-partiklene. Justerte alpha-verdiene selv for å få ønsket uttrykk.

## Hvordan jeg vurderte svarene

- Jeg leste forklaringene før jeg limte inn noe.
- Jeg testet alltid forslagene i spillet før jeg beholdt dem.
- Jeg justerte parametere (farger, alpha, fart) selv.
- Ved tvil spurte jeg om _hvorfor_, ikke bare _hvordan_.

## Hva jeg lærte

- KI er rask til å forklare og foreslå, men jeg må selv forstå koden.
- Det er viktig å stille presise spørsmål med kontekst.
- KI kan ta feil – spesielt på Pygame-versjoner og API-detaljer –
  derfor leste jeg alltid dokumentasjonen i tillegg.

# 4. Egenvurdering

## Hvor fornøyd er jeg?

Jeg er godt fornøyd med resultatet. Spillet er komplett, kjører stabilt og
føles "ferdig" – det har meny, pause, game over, highscore og en jevn
vanskelighetskurve. Jeg fikk til glød-effekter og en stemningsfull bakgrunn
som gjør at det ser bedre ut enn et typisk første-Pygame-prosjekt.

## Hva fungerer godt?

- Jevn bevegelse og responsiv input.
- Klar og tydelig HUD.
- Tre distinkte spilltilstander (meny, pause, game over).
- Highscore lagres mellom økter.
- Vanskelighetsgraden øker automatisk og holder spillet engasjerende.
- Modulær kodestruktur som er lett å utvide.

## Hva kunne vært bedre?

- Ingen lyd eller musikk – det ville hevet opplevelsen.
- Grafikken er laget av primitive former; med bilder eller animasjoner
  kunne spillet blitt mer polert.
- Power-ups (f.eks. midlertidig skjold) mangler.
- Kun ett spillmodus.

## Hva ville jeg utviklet videre med mer tid?

1. Lydeffekter for samling, kollisjon og game over.
2. Flere fiendetyper (f.eks. snøstorm, isbjørn).
3. Power-ups: skjold, magnet, dobbel poeng.
4. Uendelig modus vs. tidsbasert modus.
5. Mobilvennlig versjon med touch-input.
6. Online toppliste.

## Hvordan jobbet jeg når jeg møtte utfordringer?

Jeg prøvde alltid å **isolere problemet** først – lage en minimal versjon
av koden som viser feilen. Deretter leste jeg feilmeldinger nøye, sjekket
Pygame-dokumentasjonen, og brukte KI som sparringspartner når jeg sto fast.
Jeg testet hver løsning før jeg gikk videre.

## Brukte jeg KI? Hvordan, og hvor nyttig?

Ja, i begrenset grad. Se `03-ki-bruk.md` for detaljer. KI var mest nyttig
til å forklare Pygame-konsepter og til å peke på klassiske fallgruver
(f.eks. å endre en liste mens man itererer over den). Det var mindre nyttig
til å generere hele funksjoner – der måtte jeg uansett skrive og justere
selv for å forstå koden. Alt i alt: nyttig som hjelpelærer, men ikke som
erstatning for egen forståelse.

# 5. Ressurser

## Dokumentasjon

- Pygame offisiell dokumentasjon: https://www.pygame.org/docs/
- Python offisiell dokumentasjon: https://docs.python.org/3/

## Tutorials

- Elevkanalen – Scratch/Python: https://www.elevkanalen.no/fag/1002/produkt/2057
- Kidsa Koder (Kodeklubben): https://www.kodeklubben.no/
- Pygame "Making Games with Python & Pygame" (gratis bok av Al Sweigart):
  https://inventwithpython.com/pygame/

## Inspirasjon

- Klassiske arkadespill (Space Invaders, Snake) for enkel mekanikk.
- Nordnorsk natur og nordlys som visuelt tema.

## Verktøy

- VS Code: https://code.visualstudio.com/
- Git: https://git-scm.com/
- GitHub: https://github.com/

## KI-verktøy

- Microsoft Copilot (brukt som sparringspartner, se `03-ki-bruk.md`).
