from urllib.parse import unquote

import pytest
from conftest import RispostaFinta, SessioneFinta

from sheets import SCHEDE, ErroreFoglio, Foglio

BASE = "https://sheets.googleapis.com/v4/spreadsheets/ID_FOGLIO"


def foglio(*risposte):
    sessione = SessioneFinta(list(risposte))
    return Foglio("ID_FOGLIO", sessione), sessione


def titoli(*nomi):
    return RispostaFinta(200, {"sheets": [{"properties": {"title": n}} for n in nomi]})


def valori(righe):
    return RispostaFinta(200, {"values": righe} if righe else {})


def test_colonne_minime():
    creator, contatti = SCHEDE["Creator"], SCHEDE["Contatti"]
    for colonna in ["username", "mercato", "nicchia", "follower", "media_views_reel", "email",
                    "esito_filtri", "motivo_filtri", "stato"]:
        assert colonna in creator
    for colonna in ["username", "tipo", "id_thread", "classificazione", "prossimo_promemoria"]:
        assert colonna in contatti
    assert creator[0] == "username"


def test_prepara_schede_crea_schede_e_intestazioni_mancanti():
    f, s = foglio(titoli("Foglio1"), RispostaFinta(200), valori([]), RispostaFinta(200),
                  valori([]), RispostaFinta(200))
    f.prepara_schede()
    aggiunte = s.chiamate[1]
    assert aggiunte["url"] == BASE + ":batchUpdate"
    nomi = [r["addSheet"]["properties"]["title"] for r in aggiunte["json"]["requests"]]
    assert nomi == ["Creator", "Contatti"]
    scrittura = s.chiamate[3]
    assert scrittura["metodo"] == "PUT"
    assert unquote(scrittura["url"]).endswith("'Creator'!A1")
    assert scrittura["params"]["valueInputOption"] == "RAW"
    assert scrittura["json"]["values"] == [SCHEDE["Creator"]]


def test_prepara_schede_aggiunge_solo_colonne_mancanti_in_fondo():
    esistenti_creator = ["username", "colonna_di_manuel"] + SCHEDE["Creator"][1:-1]
    f, s = foglio(titoli("Creator", "Contatti"), valori([esistenti_creator]), RispostaFinta(200),
                  valori([SCHEDE["Contatti"]]))
    f.prepara_schede()
    assert [c["metodo"] for c in s.chiamate] == ["GET", "GET", "PUT", "GET"]
    scrittura = s.chiamate[2]
    colonna = len(esistenti_creator) + 1
    assert unquote(scrittura["url"]).endswith(f"'Creator'!{Foglio.lettera(colonna)}1")
    assert scrittura["json"]["values"] == [[SCHEDE["Creator"][-1]]]


def test_leggi_restituisce_dizionari_con_numero_di_riga():
    f, s = foglio(valori([["username", "follower", "note"], ["anna", "25000"], [], ["bea", "", "ok"]]))
    righe = f.leggi("Creator")
    assert righe == [
        {"_riga": 2, "username": "anna", "follower": "25000", "note": ""},
        {"_riga": 4, "username": "bea", "follower": "", "note": "ok"},
    ]
    assert unquote(s.chiamate[0]["url"]).endswith("/values/'Creator'")


def test_leggi_scheda_vuota():
    f, _ = foglio(valori([]))
    assert f.leggi("Contatti") == []


def test_aggiungi_righe_nell_ordine_delle_intestazioni():
    f, s = foglio(valori([["username", "tipo", "note"]]), RispostaFinta(200))
    f.aggiungi("Contatti", [{"note": "=HYPERLINK(\"x\")", "username": "anna"}, {"tipo": "prova", "username": None}])
    chiamata = s.chiamate[1]
    assert chiamata["metodo"] == "POST"
    assert unquote(chiamata["url"]).endswith("/values/'Contatti'!A1:append")
    assert chiamata["params"]["valueInputOption"] == "RAW"  # niente formule eseguite
    assert chiamata["params"]["insertDataOption"] == "INSERT_ROWS"
    assert chiamata["json"]["values"] == [["anna", "", "=HYPERLINK(\"x\")"], ["", "prova", ""]]


def test_aggiungi_colonna_sconosciuta():
    f, _ = foglio(valori([["username"]]))
    with pytest.raises(ValueError, match="sconosciuta"):
        f.aggiungi("Contatti", [{"username": "a", "inventata": 1}])


def test_aggiorna_scrive_solo_le_celle_indicate():
    f, s = foglio(valori([["username", "follower", "note", "stato"]]), RispostaFinta(200))
    f.aggiorna("Creator", 5, {"follower": 25000, "stato": "da contattare"})
    chiamata = s.chiamate[1]
    assert chiamata["url"] == BASE + "/values:batchUpdate"
    assert chiamata["json"]["valueInputOption"] == "RAW"
    assert chiamata["json"]["data"] == [
        {"range": "'Creator'!B5", "values": [[25000]]},
        {"range": "'Creator'!D5", "values": [["da contattare"]]},
    ]


def test_aggiorna_non_tocca_le_intestazioni():
    f, _ = foglio()
    with pytest.raises(ValueError, match="riga"):
        f.aggiorna("Creator", 1, {"stato": "x"})


def test_scheda_non_prevista():
    f, _ = foglio()
    with pytest.raises(ValueError, match="scheda"):
        f.leggi("Altro")


def test_lettera_colonna():
    assert [Foglio.lettera(n) for n in (1, 26, 27, 52, 703)] == ["A", "Z", "AA", "AZ", "AAA"]


@pytest.mark.parametrize(
    "status, testo",
    [(403, "condiviso"), (404, "SHEET_ID"), (500, "errore 500")],
)
def test_errori_google(status, testo):
    f, _ = foglio(RispostaFinta(status, {"error": {"message": "dettaglio Google"}}))
    with pytest.raises(ErroreFoglio, match=testo):
        f.leggi("Creator")


def test_sheet_id_non_valido():
    with pytest.raises(ValueError):
        Foglio("id/../altro", SessioneFinta())


def test_credenziali_non_json():
    from sheets import sessione_account_servizio

    with pytest.raises(ErroreFoglio, match="JSON"):
        sessione_account_servizio("/percorso/del/file.json")


def test_credenziali_tra_apici_singoli(monkeypatch):
    from google.oauth2 import service_account

    import sheets

    ricevute = {}
    monkeypatch.setattr(service_account.Credentials, "from_service_account_info",
                        lambda info, scopes: ricevute.setdefault("info", info))
    monkeypatch.setattr("google.auth.transport.requests.AuthorizedSession", lambda c: c)
    sheets.sessione_account_servizio('  \'{"type": "service_account"}\'  ')
    assert ricevute["info"] == {"type": "service_account"}
