"""Schede Creator e Contatti del Foglio Google, con un account di servizio."""
import json
import re
from urllib.parse import quote

API = "https://sheets.googleapis.com/v4/spreadsheets"
SCOPE = "https://www.googleapis.com/auth/spreadsheets"
TIMEOUT = 30

SCHEDE = {
    # Una riga per creator. Manuel scrive username, mercato e nicchia; il resto lo compila il sistema.
    "Creator": [
        "username", "mercato", "nicchia", "aggiunto_il",
        "nome", "bio", "sito", "follower", "numero_post",
        "media_like", "media_commenti", "media_views_reel",
        "email", "esito_filtri", "motivo_filtri", "dati_aggiornati_il",
        "stato", "note",
    ],
    # Una riga per messaggio: primo contatto, promemoria, replica, risposta ricevuta.
    "Contatti": [
        "creata_il", "username", "email", "tipo", "oggetto",
        "id_bozza", "id_thread", "inviata_il",
        "classificazione", "prossimo_promemoria", "note",
    ],
}


class ErroreFoglio(Exception):
    pass


def sessione_account_servizio(credenziali_json: str):
    """Sessione HTTP autenticata con il JSON dell'account di servizio (contenuto, non percorso)."""
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account

    testo = credenziali_json.strip()
    if len(testo) > 1 and testo[0] == testo[-1] == "'":  # incollato tra apici singoli
        testo = testo[1:-1]
    try:
        info = json.loads(testo)
    except ValueError:
        raise ErroreFoglio("GOOGLE_SERVICE_ACCOUNT_JSON non è un JSON valido: incolla tutto il file") from None
    credenziali = service_account.Credentials.from_service_account_info(info, scopes=[SCOPE])
    return AuthorizedSession(credenziali)


class Foglio:
    def __init__(self, sheet_id: str, sessione):
        if not re.fullmatch(r"[A-Za-z0-9_-]+", sheet_id or ""):
            raise ValueError("SHEET_ID non valido: copia solo la parte tra /d/ e /edit dell'indirizzo")
        self.base = f"{API}/{sheet_id}"
        self.sessione = sessione

    def prepara_schede(self) -> None:
        """Crea le schede e le intestazioni mancanti; le colonne aggiunte a mano restano."""
        dati = self._chiama("GET", self.base, params={"fields": "sheets.properties.title"})
        esistenti = {s["properties"]["title"] for s in dati.get("sheets", [])}
        nuove = [n for n in SCHEDE if n not in esistenti]
        if nuove:
            richieste = [{"addSheet": {"properties": {"title": n}}} for n in nuove]
            self._chiama("POST", f"{self.base}:batchUpdate", json={"requests": richieste})
        for scheda, colonne in SCHEDE.items():
            presenti = self.intestazioni(scheda)
            mancanti = [c for c in colonne if c not in presenti]
            if mancanti:
                inizio = f"{_rif(scheda)}!{self.lettera(len(presenti) + 1)}1"
                self._scrivi(inizio, [mancanti])

    def intestazioni(self, scheda: str) -> list[str]:
        valori = self._valori(f"{_rif(scheda)}!1:1")
        return valori[0] if valori else []

    def leggi(self, scheda: str) -> list[dict]:
        """Righe non vuote come dizionari, con il numero di riga in `_riga`."""
        valori = self._valori(_rif(scheda))
        if not valori:
            return []
        intestazioni, righe = valori[0], []
        for numero, riga in enumerate(valori[1:], start=2):
            if any(str(v).strip() for v in riga):
                riga = riga + [""] * (len(intestazioni) - len(riga))
                righe.append({"_riga": numero, **dict(zip(intestazioni, riga))})
        return righe

    def aggiungi(self, scheda: str, righe: list[dict]) -> None:
        intestazioni = self.intestazioni(scheda)
        for riga in righe:
            sconosciute = set(riga) - set(intestazioni)
            if sconosciute:
                raise ValueError(f"colonna sconosciuta in {scheda}: {', '.join(sorted(sconosciute))}")
        valori = [["" if r.get(c) is None else r.get(c) for c in intestazioni] for r in righe]
        self._chiama(
            "POST", f"{self.base}/values/{quote(_rif(scheda) + '!A1', safe='')}:append",
            params={"valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"},
            json={"values": valori},
        )

    def aggiorna(self, scheda: str, numero_riga: int, campi: dict) -> None:
        """Scrive solo le celle indicate, senza toccare le altre colonne della riga."""
        if numero_riga < 2:
            raise ValueError("la riga 1 contiene le intestazioni: indica una riga dalla 2 in poi")
        intestazioni = self.intestazioni(scheda)
        dati = []
        for colonna, valore in campi.items():
            if colonna not in intestazioni:
                raise ValueError(f"colonna sconosciuta in {scheda}: {colonna}")
            cella = f"{_rif(scheda)}!{self.lettera(intestazioni.index(colonna) + 1)}{numero_riga}"
            dati.append({"range": cella, "values": [["" if valore is None else valore]]})
        self._chiama("POST", f"{self.base}/values:batchUpdate",
                     json={"valueInputOption": "RAW", "data": dati})

    @staticmethod
    def lettera(numero: int) -> str:
        """Numero di colonna (1 = A) in lettere."""
        lettere = ""
        while numero:
            numero, resto = divmod(numero - 1, 26)
            lettere = chr(65 + resto) + lettere
        return lettere

    def _valori(self, intervallo: str) -> list[list]:
        return self._chiama("GET", f"{self.base}/values/{quote(intervallo, safe='')}").get("values", [])

    def _scrivi(self, intervallo: str, valori: list[list]) -> None:
        self._chiama("PUT", f"{self.base}/values/{quote(intervallo, safe='')}",
                     params={"valueInputOption": "RAW"}, json={"values": valori})

    def _chiama(self, metodo: str, url: str, **kwargs) -> dict:
        # RAW ovunque: un testo che inizia con "=" (per esempio in una bio) resta testo, non formula.
        risposta = getattr(self.sessione, metodo.lower())(url, timeout=TIMEOUT, **kwargs)
        try:
            dati = risposta.json()
        except ValueError:
            dati = {}
        if risposta.status_code >= 400:
            dettaglio = (dati.get("error") or {}).get("message", "")
            if risposta.status_code == 403:
                raise ErroreFoglio(f"accesso negato: il foglio non è condiviso con l'account di servizio ({dettaglio})")
            if risposta.status_code == 404:
                raise ErroreFoglio(f"foglio non trovato: controlla SHEET_ID ({dettaglio})")
            raise ErroreFoglio(f"errore {risposta.status_code} da Google Sheets ({dettaglio})")
        return dati


def _rif(scheda: str) -> str:
    if scheda not in SCHEDE:
        raise ValueError(f"scheda non prevista: {scheda!r} (valide: {', '.join(SCHEDE)})")
    return f"'{scheda}'"
