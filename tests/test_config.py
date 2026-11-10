import pytest

from config import ErroreConfigurazione, carica_profilo, variabile


@pytest.mark.parametrize("mercato", ["it", "en"])
def test_profili_di_mercato_completi(mercato):
    profilo = carica_profilo(mercato)
    assert profilo["mercato"] == mercato
    assert profilo["lingua"] and profilo["tono"]
    soglie = profilo["soglie"]
    assert soglie["follower_min"] == 10000
    assert soglie["follower_max"] == 100000
    assert soglie["follower_max_confronto"] == 300000
    assert soglie["rapporto_min_views_follower"] == 0.1
    assert profilo["parole_prodotto"] and profilo["domini_vendita"]
    assert profilo["prezzi_indicativi"]["valuta"]


def test_mercato_sconosciuto():
    with pytest.raises(ErroreConfigurazione, match="mercato"):
        carica_profilo("fr")


def test_variabile_presente(monkeypatch):
    monkeypatch.setenv("SHEET_ID", "  abc123 ")
    assert variabile("SHEET_ID") == "abc123"


def test_variabile_mancante_rimanda_alla_guida(monkeypatch):
    monkeypatch.delenv("SHEET_ID", raising=False)
    with pytest.raises(ErroreConfigurazione, match="SHEET_ID.*SETUP"):
        variabile("SHEET_ID")


def test_nicchie_csv_ha_solo_intestazioni():
    from config import RADICE

    righe = (RADICE / "data" / "nicchie.csv").read_text().splitlines()
    assert len(righe) == 1
    colonne = righe[0].split(",")
    for criterio in [
        "disponibilita_pagare", "urgenza", "creator_disponibili", "durata_bisogno",
        "ricambio_pubblico", "potere_acquisto", "fattibilita", "concorrenza",
    ]:
        assert f"{criterio}_voto" in colonne and f"{criterio}_prove" in colonne
    for colonna in ["nicchia", "mercato", "punteggio_base", "moltiplicatore_rischio",
                    "punteggio_finale", "affidabilita"]:
        assert colonna in colonne
