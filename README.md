# LeetCode Solver

Rezolva probleme LeetCode automat via clipboard + hotkey, folosind Gemini AI.

## Setup (o singura data)

```powershell
git clone git@github.com:RaduAndreiTudorica/solver.git
cd leetcode-solver
.\setup.ps1
```

Scriptul de setup:
- Verifica Python si il detecteaza automat (`python` sau `py`)
- Creeaza un virtual environment `.venv`
- Instaleaza toate dependentele din `requirements.txt`
- Te intreaba de `GEMINI_API_KEY` si il salveaza permanent

> API key gratuit de pe [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

## Rulare

```powershell
.\run.ps1
```

> **Important:** Ruleaza PowerShell ca **Administrator** pentru ca hotkey-urile sa functioneze in orice aplicatie (inclusiv browser).

## Utilizare

1. Pe LeetCode, selecteaza tot enuntul problemei → `Ctrl+C` → `Ctrl+Shift+L`
2. In editorul LeetCode, selecteaza template-ul functiei → `Ctrl+C` → `Ctrl+Shift+K`
3. Asteapta ~3-5 secunde
4. `Ctrl+V` in editor — solutia C++ e in clipboard

## Hotkeys

| Hotkey | Actiune |
|--------|---------|
| `Ctrl+Shift+L` | Salveaza enuntul din clipboard |
| `Ctrl+Shift+K` | Trimite enunt + antet la Gemini si pune solutia in clipboard |

## Modele disponibile

In `script.py`, linia `MODEL`:
- `gemini-2.5-flash` — gratuit, rapid, suficient pentru easy/medium
- `gemini-2.5-pro` — mai bun la hard, necesita billing activat

## .gitignore

`.venv/` e exclus automat — fiecare utilizator isi face propriul venv dupa clone.
