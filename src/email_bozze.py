"""Bozze email. In sessione la bozza la crea Claude con il connettore Gmail.

Per passare a un server basta implementare questa funzione con l'API di Gmail:
il resto del codice usa solo questa interfaccia.
"""


def crea_bozza_email(destinatario: str, oggetto: str, corpo: str) -> str:
    """Crea una bozza in Gmail e restituisce il suo id."""
    raise NotImplementedError(
        "nessuna implementazione nel codice: in sessione la bozza la crea Claude con il connettore Gmail"
    )
