# Simulator de zaruri și jocuri de noroc

Acest proiect este un simulator de zaruri realizat în Python, care permite simulări statistice, calcul de probabilități și rularea unor jocuri de noroc clasice. Aplicația rulează din linia de comandă și este containerizată folosind Docker.

---

## Funcționalități

- simularea aruncărilor de zar cu un număr configurabil de fețe
- afișarea distribuției rezultatelor și histogramă ASCII
- calculul statisticilor: medie, mediană, deviație standard
- calculul probabilităților experimentale și teoretice pentru sume
- simularea jocurilor Craps și Yahtzee
- salvarea rezultatelor într-un fișier text

---

## Structura proiectului

├── cod_full.py
├── Dockerfile
└── README.md

---

## Cerințe

- Docker instalat  
https://docs.docker.com/get-docker/

Nu este necesară instalarea Python pe sistemul local.

---

## Rulare cu Docker

### Construirea imaginii Docker

```bash
docker build -t dice-simulator .
```
Rulare implicită (simulare simplă)
```bash
docker run --rm dice-simulator
```
Argumente disponibile
| Argument  | Descriere                                      |
| --------- | ---------------------------------------------- |
| `--faces` | Numărul de fețe ale zarului (6, 8, 10, 12, 20) |
| `--dice`  | Numărul de zaruri                              |
| `--rolls` | Numărul de simulări                            |
| `--seed`  | Seed pentru generatorul random                 |
| `--prob`  | Sumă țintă pentru calculul probabilității      |
| `--game`  | Joc (`craps`, `yahtzee`, `sum`)                |
| `--save`  | Salvează rezultatul într-un fișier             |
| `--out`   | Numele fișierului de output                    |

Exemple de rulare:
Simulare simplă
```bash
docker run --rm dice-simulator --faces 6 --rolls 5000
```
Calcul probabilitate pentru o sumă
```bash
docker run --rm dice-simulator --faces 6 --dice 2 --rolls 10000 --prob 7
```
Joc Craps
```bash
docker run --rm dice-simulator --game craps --rolls 10000
```
Joc Yahtzee
```bash
docker run --rm dice-simulator --game yahtzee --rolls 50000
```
Joc simplu de comparare a sumelor
```bash
docker run --rm dice-simulator --game sum --dice 2 --faces 6
```
Salvarea rezultatului
```bash
docker run --rm dice-simulator --save
```
Fișierul rezultat este salvat automat cu un nume de forma:
dice_log_YYYYMMDD_HHMMSS.txt
