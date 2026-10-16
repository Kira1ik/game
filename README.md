# Nordlysjeger

Et 2D-arkadespill laget i Python med Pygame. Spilleren samler
nordlys-partikler og unngår iskrystaller. Tre liv, økende
vanskelighetsgrad, power-ups og highscore.

## Kontroller

| Tast             | Handling         |
| ---------------- | ---------------- |
| Piltaster / WASD | Bevegelse        |
| P / ESC          | Pause            |
| ENTER            | Start / restart  |
| Q                | Tilbake til meny |

## Mekanikker

- Nordlys: +10 poeng
- Iskrystall: −1 liv
- Skjold: 6 sek usårbar
- Magnet: 7 sek tiltrekning
- Slow-motion: 4 sek saktere
- Combo og nivåøkning hvert 20. sek

## Verktøy

Python 3, Pygame-CE, VS Code, Git

## Utfordringer

- Diagonalbevegelse for rask → skalert med 0,707
- Objekter forsvant ikke → itererte over kopi av listen
- Pygame installerte ikke → byttet til pygame-ce

## KI-bruk

Brukt i liten grad, kun for å forstå feilmeldinger. All kode
skrevet og testet selv.

## Egenvurdering

Fornøyd. Fungerer stabilt med flere mekanikker. Kunne hatt
bedre grafikk og flere fiendetyper.

## Ressurser

- https://www.pygame.org/docs/
- https://docs.python.org/3/
- https://www.kodeklubben.no/
