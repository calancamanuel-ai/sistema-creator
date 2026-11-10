import pytest

from email_bozze import crea_bozza_email


def test_crea_bozza_email_solo_interfaccia():
    with pytest.raises(NotImplementedError, match="connettore Gmail"):
        crea_bozza_email(destinatario="prova@example.com", oggetto="Ciao", corpo="Testo")
