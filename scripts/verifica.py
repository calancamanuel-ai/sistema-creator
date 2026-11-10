#!/usr/bin/env python3
"""Verifica della fase 0 con le credenziali vere.

Legge il foglio (creando schede e intestazioni se mancano), scrive una riga di prova
nella scheda Contatti e chiama Business Discovery sul nome utente indicato.

Uso:  python scripts/verifica.py NOME_UTENTE [--mercato it|en]
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import requests  # noqa: E402
from google.auth.exceptions import GoogleAuthError  # noqa: E402

from config import MERCATI, ErroreConfigurazione, carica_profilo, variabile  # noqa: E402
from filtri import applica_filtri  # noqa: E402
from instagram import ErroreInstagram, dati_account, trova_ig_user_id  # noqa: E402
from sheets import ErroreFoglio, Foglio, sessione_account_servizio  # noqa: E402

ERRORI = (ErroreConfigurazione, ErroreFoglio, ErroreInstagram, GoogleAuthError,
          requests.RequestException, ValueError)


def verifica_foglio() -> None:
    sessione = sessione_account_servizio(variabile("GOOGLE_SERVICE_ACCOUNT_JSON"))
    foglio = Foglio(variabile("SHEET_ID"), sessione)
    foglio.prepara_schede()
    creator, contatti = foglio.leggi("Creator"), foglio.leggi("Contatti")
    print(f"  schede pronte; letti {len(creator)} creator e {len(contatti)} contatti")
    ora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    foglio.aggiungi("Contatti", [{
        "creata_il": ora, "username": "prova_verifica", "tipo": "prova",
        "note": "riga di prova di scripts/verifica.py: puoi cancellarla",
    }])
    print("  scritta una riga di prova nella scheda Contatti")


def verifica_instagram(username: str, mercato: str) -> None:
    token = variabile("IG_ACCESS_TOKEN")
    try:
        ig_user_id = variabile("IG_USER_ID")
    except ErroreConfigurazione:
        pagine = trova_ig_user_id(token=token)
        for pagina, ig_id in pagine:
            print(f"  pagina '{pagina}': IG_USER_ID = {ig_id}")
        if not pagine:
            print("  il token non vede nessuna pagina collegata a un account Instagram professionale")
        raise
    profilo = carica_profilo(mercato)
    account = dati_account(username, token=token, ig_user_id=ig_user_id,
                           n_post=profilo["soglie"]["post_recenti_da_analizzare"])
    reel = [p for p in account.post if p.tipo == "REELS" and p.visualizzazioni is not None]
    print(f"  @{account.username}: {account.follower} follower, {account.numero_post} post")
    print(f"  letti {len(account.post)} post recenti, di cui {len(reel)} Reel con visualizzazioni")
    print(f"  bio: {account.bio[:80]!r}  sito: {account.sito or '-'}")
    esito = applica_filtri(account, profilo)
    print(f"  filtri ({mercato}): {esito.esito} - {esito.motivo}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("username", help="nome utente Instagram di un account professionale")
    parser.add_argument("--mercato", choices=MERCATI, default="it")
    args = parser.parse_args()

    riuscite = True
    for nome, controllo in (("Foglio Google", verifica_foglio),
                            ("Instagram", lambda: verifica_instagram(args.username, args.mercato))):
        print(f"{nome}:")
        try:
            controllo()
            print("  OK")
        except ERRORI as errore:
            print(f"  ERRORE: {errore}")
            riuscite = False
    return 0 if riuscite else 1


if __name__ == "__main__":
    sys.exit(main())
