"""Variabili d'ambiente e profili di mercato."""
import os
from pathlib import Path

import yaml

RADICE = Path(__file__).resolve().parent.parent
MERCATI = ("it", "en")


class ErroreConfigurazione(Exception):
    pass


def variabile(nome: str) -> str:
    """Valore di una variabile d'ambiente obbligatoria (i segreti stanno solo lì)."""
    valore = os.environ.get(nome, "").strip()
    if not valore:
        raise ErroreConfigurazione(f"Manca la variabile d'ambiente {nome}: vedi docs/SETUP.md")
    return valore


def carica_profilo(mercato: str) -> dict:
    """Profilo del mercato da config/markets/<mercato>.yaml."""
    if mercato not in MERCATI:
        raise ErroreConfigurazione(f"mercato sconosciuto: {mercato!r} (validi: {', '.join(MERCATI)})")
    percorso = RADICE / "config" / "markets" / f"{mercato}.yaml"
    return yaml.safe_load(percorso.read_text(encoding="utf-8"))
