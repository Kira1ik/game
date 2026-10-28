# Dokumentasjon og Arbeidslogg: Nordlysjeger

**Elev:** Zhanna
**Fag:** Programmering og spillutvikling
**Periode:** 3 onsdeger + eget arbeid hjemme

---

## onsdag 14 : Planlegging og oppsett

**Mål for økten:** Bestemme ideen, velge verktøy og få et grunnleggende vindu på skjermen.

**Hva jeg gjorde:**
Jeg startet med å bestemme meg for hva spillet skulle handle om. Jeg ville lage noe med et tydelig norsk preg. Valget falt på nordlys, fordi det er visuelt kult og lar meg bruke mørke farger med sterke neon-aksenter (grønn, blå, lilla).

Målet med spillet ble raskt definert: Spilleren skal bevege seg fritt, samle nordlys-partikler for poeng, og unngå iskrystaller som faller ned. Jeg bestemte meg for at det skulle være 3 liv, og at farten skulle øke over tid for å gjøre det vanskeligere.

Jeg valgte å bruke **Python med Pygame**. Jeg vurderte Unity, men siden jeg allerede kunne litt Python, følte jeg at Pygame var lettere å få til i løpet av de tre øktene. Jeg opprettet prosjektmappen i VS Code og lagde en tom fil (`main.py`). Her skrev jeg koden for å starte Pygame, sette opp vinduet (800x600) og få en `while`-løkke til å kjøre i 60 FPS.

**Utfordring:**
Da jeg skulle installere Pygame, fikk jeg en stor feilmelding i terminalen. Det viste seg at den vanlige `pygame`-pakken ikke støttet den nyeste Python-versjonen min. Jeg fant ut at jeg måtte bruke `pygame-ce` (Community Edition) i stedet. Etter det fungerte alt.

---

## osdag 21: Utvikling av kjernefunksjonalitet

**Mål for økten:** Få spilleren til å bevege seg, få objekter til å falle, og få kollisjoner til å fungere.

**Hva jeg gjorde:**
Jeg begynte å lage klassen `Player`. Først fikk jeg en firkant til å bevege seg med piltastene, men jeg byttet det raskt ut med en sirkel for å få en mer "åndelig" look. Jeg la inn glødeeffekter rundt spilleren ved hjelp av halvgjennomsiktige sirkler.

Deretter lagde jeg klassene `Nordlys` og `Iskrystall`. Jeg la inn en timer (spawn_timer) som bestemmer hvor ofte de skal dukke opp på toppen av skjermen. Jeg fikk dem til å falle nedover i varierende hastighet.

Så kom den viktigste delen: **Kollisjoner**. Jeg brukte `pygame.Rect` og `colliderect()` for å sjekke om spilleren traff et objekt. Hvis spilleren traff nordlys, økte jeg poengsummen med 10 og fjernet nordlyset. Hvis spilleren traff is, trakk jeg fra ett liv.

**Utfordringer underveis:**

1. **Diagonal-bevegelse:** Jeg merket at hvis jeg holdt inne to piltaster samtidig (f.eks. opp og høyre), gikk spilleren mye fortere enn vanlig. Jeg googlet det og fant ut at jeg måtte normalisere bevegelsen. Jeg fikset det ved å gange farten med 0.7071 når man beveget seg diagonalt.
2. **Objekter som ikke forsvant:** Når nordlys eller is gikk utenfor skjermen, ble de hengende fast i minnet. Jeg prøvde å fjerne dem fra listen min, men da kræsjet spillet eller hoppet over objekter. Jeg skjønte at man ikke kan fjerne elementer fra en liste mens man går gjennom den. Jeg løste det ved å gå gjennom en kopi av listen (`for x in liste[:]`).

Mot slutten av økten la jeg til en Highscore-funksjon som lagrer poengsummen til en tekstfil (`highscore.txt`), og et Game Over-vindu.

---

## onsdag 28: Polering, feilsøking og eget arbeid hjemme

**Mål for økten:** Gjøre spillet morsommere med power-ups, legge til menyer og finpusse koden.

**Hva jeg gjorde (på skolen og hjemme):**
Spillet fungerte, men det ble litt kjedelig i lengden. Derfor bestemte jeg meg for å legge til **Power-ups**. Jeg lagde tre typer:

- Skjold (spilleren blir udyrbar)
- Magnet (drar til seg nordlys)
- Slow-motion (alt går saktere)

Dette krevde at jeg lagde nedtellings-timere i `Player`-klassen som sier hvor mange frames effekten skal vare (f.eks. 6 sekunder = 360 frames).

**Arbeid hjemme:**
Jeg innså ganske raskt at 3 økter på skolen ikke var nok for å bli helt ferdig med alt jeg ville. Derfor jobbet jeg en god del med prosjektet hjemme på kveldstid. Det var hjemme jeg fikk tid til å sitte skikkelig med feilsøking og rydde i koden. Jeg flyttet alt av innstillinger (farger, skjermstørrelse, hastigheter) til en egen fil (`settings.py`), og delte opp resten i moduler (som `objects.py` og `player.py`). Dette gjorde filene mye kortere og lettere å lese.

Til slutt la jeg til et Start-meny og en Pause-funksjon (ved å trykke P), slik at spillet føles mer komplett. Å jobbe hjemme gjorde at jeg fikk brukt mye mer tid på detaljer, som glødeeffekter og hvordan menyen skulle se ut.

---

## Bruk av ressurser og KI

For å få til dette prosjektet har jeg brukt flere typer ressurser aktivt.

**YouTube og tutorials:**
Siden jeg aldri hadde laget et Pygame-spill før, brukte jeg mye YouTube. Jeg så videoer fra kanaler som _freeCodeCamp_ og _Tech With Tim_. Jeg så spesielt på videoer som forklarte hvordan man setter opp en spill-løkke, hvordan man bruker klasser i Python, og hvordan man håndterer kollisjoner og input. Tutorialsene ga meg en grunnmur, men jeg måtte tilpasse alt til mitt eget spill.

**Bruk av KI:**
Jeg skrev og testet absolutt all kode selv, men jeg brukte KI (som Microsoft Copilot) som en _hjelpelærer_ når jeg sto fast. Jeg brukte det aldri til å generere hele spillet, men heller til å forstå feilmeldinger og finne riktig tilnærming.

_Eksempler på hva jeg spurte KI om:_

1. _"Hvordan kan jeg sørge for at diagonal bevegelse ikke blir raskere enn vanlig bevegelse i Pygame?"_ (Fikk forklart at jeg måtte gange med 0.7071).
2. _"Vanlig pygame feiler under installasjon på den nye Python-versjonen min. Hva er løsningen?"_ (Fikk tips om å bytte til `pygame-ce`).
3. _"Hva er den beste måten å lage en Pause-funksjon i en while-løkke?"_ (Fikk tips om å bruke en `game_state`-variabel i stedet for å stoppe løkken helt).

_Hvordan jeg bearbeidet svarene:_
Jeg leste alltid forklaringene fra KI for å forstå _hvorfor_ det fungerte, og testet deretter løsningene i min egen kode. Jeg merket at KI noen ganger foreslo løsninger som ikke passet helt med strukturen min. Da måtte jeg justere det selv. Jeg lærte at KI er et kjempebra verktøy for å komme videre når man står fast, men at man må forstå koden selv for at det skal bli bra.

---

## Testing

Jeg spilte spillet mange ganger selv for å teste.

- Fungerer kollisjonene riktig? (Ja)
- Lagres rekorden når jeg dør? (Ja)
- Kan man jukse ved å holde seg i et hjørne? (Jeg la inn kode som gjør at iskrystallene faller i hele bredden, så det er vanskelig).
- Fungerer pausefunksjonen? (Ja)

---

## Oppsummering av arbeidsprosessen

Jeg har lært utrolig mye av å jobbe med dette prosjektet. Jeg har gått fra å bare kunne grunnleggende Python til å forstå hvordan man bygger opp et objektorientert system med klasser, hvordan man håndterer kollisjoner i 2D, og hvordan man feilsøker kode som ikke gjør som man vil.

Den største lærdommen er at det å dele koden inn i mindre filer (moduler) er helt avgjørende når prosjektet vokser. Det gjorde feilsøkingen mye enklere på slutten. Jeg har også lært at det å jobbe hjemme og oppsøke hjelp (både via YouTube og KI) når man står fast, er helt nødvendig for å bli ferdig med et større prosjekt.

Hvis jeg skulle gjort dette igjen, ville jeg ha tegnet mer grafikk selv (f.eks. sprites) i stedet for å bruke geometriske figurer, men jeg er godt fornøyd med resultatet og følelsen spillet gir.
