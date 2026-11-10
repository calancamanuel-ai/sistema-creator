"""Sessione HTTP simulata: registra le chiamate e restituisce risposte preparate."""
import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


class RispostaFinta:
    def __init__(self, status_code=200, dati=None):
        self.status_code = status_code
        self._dati = {} if dati is None else dati

    def json(self):
        if isinstance(self._dati, Exception):
            raise self._dati
        return self._dati


class SessioneFinta:
    """Sostituisce requests.Session / AuthorizedSession nei test."""

    def __init__(self, risposte=None):
        self.risposte = list(risposte or [])
        self.chiamate = []

    def _rispondi(self, metodo, url, **kwargs):
        self.chiamate.append({"metodo": metodo, "url": url, **kwargs})
        if not self.risposte:
            return RispostaFinta(200, {})
        return self.risposte.pop(0)

    def get(self, url, **kwargs):
        return self._rispondi("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self._rispondi("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self._rispondi("PUT", url, **kwargs)


@pytest.fixture
def business_discovery():
    return json.loads((FIXTURES / "business_discovery.json").read_text())
