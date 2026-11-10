# sistema-creator

Piano 1: trovare creator e creare ebook. Il piano completo è in `docs/piano-1-creator-ebook.md`,
la configurazione in `docs/SETUP.md`.

| Cartella | Contenuto |
| --- | --- |
| `src/` | Codice: `instagram`, `sheets`, `filtri`, `email_bozze`, `config` |
| `prompts/` | Istruzioni per Claude |
| `config/markets/` | Profili di mercato (`it.yaml`, `en.yaml`): lingua, tono, soglie, prezzi |
| `data/` | `nicchie.csv`: classifica delle nicchie (nessun dato personale) |
| `tests/` | Test con risposte simulate, senza chiamate reali |
| `scripts/` | `verifica.py`: prova con le credenziali vere |

```
pip install -r requirements.txt
python -m pytest
python scripts/verifica.py NOME_UTENTE [--mercato en]
```

I segreti si leggono solo dalle variabili d'ambiente `GOOGLE_SERVICE_ACCOUNT_JSON`, `SHEET_ID`,
`IG_ACCESS_TOKEN`, `IG_USER_ID`. I dati su creator e contatti stanno solo nel Foglio Google.
