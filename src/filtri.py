"""Filtri dei creator secondo le soglie del profilo di mercato."""
import re
from dataclasses import dataclass

from instagram import Account

PASSA, DA_VERIFICARE, SCARTATO = "passa", "da verificare", "scartato"
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


@dataclass(frozen=True)
class Esito:
    esito: str  # PASSA, DA_VERIFICARE o SCARTATO
    motivo: str


def trova_email(testo: str) -> str:
    trovata = EMAIL.search(testo or "")
    return trovata.group(0) if trovata else ""


def applica_filtri(account: Account, profilo: dict, email: str = "") -> Esito:
    """Esito e motivo. `email` è quella scritta nel foglio, se c'è; altrimenti si cerca nella bio."""
    soglie = profilo["soglie"]
    scarti, dubbi, note = [], [], []

    f = account.follower
    if f < soglie["follower_min"]:
        scarti.append(f"follower {_n(f)} sotto la soglia di {_n(soglie['follower_min'])}")
    elif f > soglie["follower_max_confronto"]:
        scarti.append(f"follower {_n(f)} sopra il massimo di {_n(soglie['follower_max_confronto'])}")
    elif f > soglie["follower_max"]:
        note.append(f"fascia di confronto ({_n(soglie['follower_max'])}-{_n(soglie['follower_max_confronto'])})")

    views = [p.visualizzazioni for p in account.post if p.tipo == "REELS" and p.visualizzazioni is not None]
    if not views:
        dubbi.append("nessun Reel con visualizzazioni tra i post recenti")
    else:
        media, minimo = sum(views) / len(views), f * soglie["rapporto_min_views_follower"]
        if media < minimo:
            scarti.append(f"visualizzazioni medie dei Reel {_n(media)} sotto il minimo di {_n(minimo)}")

    for dove, testo in (("nella bio", account.bio), ("nel sito", account.sito)):
        segnale = _segnale_prodotto(testo, profilo)
        if segnale:
            scarti.append(f"possibile prodotto proprio: '{segnale}' {dove}")
    segnale = _segnale_prodotto(" \n ".join(p.didascalia for p in account.post), profilo)
    if segnale:
        dubbi.append(f"'{segnale}' nelle didascalie: controlla se vende un prodotto proprio")

    if not (email.strip() or trova_email(account.bio)):
        dubbi.append("email business non trovata nella bio: copiala dal profilo nella colonna email")

    if scarti:
        return Esito(SCARTATO, "; ".join(scarti + dubbi))
    if dubbi:
        return Esito(DA_VERIFICARE, "; ".join(dubbi + note))
    return Esito(PASSA, "; ".join(note) or "tutti i filtri superati")


def _segnale_prodotto(testo: str, profilo: dict) -> str:
    testo = (testo or "").lower()
    for dominio in profilo["domini_vendita"]:
        if dominio in testo:
            return dominio
    for parola in profilo["parole_prodotto"]:
        if re.search(rf"(?<!\w){re.escape(parola)}(?!\w)", testo):
            return parola
    return ""


def _n(numero: float) -> str:
    return f"{round(numero):,}".replace(",", ".")
