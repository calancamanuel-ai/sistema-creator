"""Dati pubblici di un account Instagram professionale tramite Business Discovery."""
import re
from dataclasses import dataclass

import requests

API = "https://graph.facebook.com/v27.0"
CAMPI_POST = (
    "id,caption,like_count,comments_count,view_count,"
    "media_type,media_product_type,permalink,timestamp"
)
NOME_UTENTE = re.compile(r"^[A-Za-z0-9._]{1,30}$")
TIMEOUT = 30


class ErroreInstagram(Exception):
    pass


@dataclass(frozen=True)
class Post:
    id: str
    didascalia: str
    like: int | None
    commenti: int | None
    visualizzazioni: int | None  # solo per i Reel
    tipo: str  # media_product_type: FEED, REELS, ...
    data: str
    link: str


@dataclass(frozen=True)
class Account:
    username: str
    nome: str
    bio: str
    sito: str
    follower: int
    numero_post: int
    post: tuple[Post, ...]


def dati_account(username: str, *, token: str, ig_user_id: str, sessione=None, n_post: int = 12) -> Account:
    """Follower, numero di post, ultimi n_post post, bio e sito di un account professionale."""
    username = username.strip().lstrip("@")
    if not NOME_UTENTE.match(username):
        raise ValueError(f"nome utente Instagram non valido: {username!r}")
    if not ig_user_id.isdigit():
        raise ValueError("IG_USER_ID deve contenere solo cifre")
    campi = (
        f"business_discovery.username({username})"
        f"{{username,name,biography,website,followers_count,media_count,"
        f"media.limit({int(n_post)}){{{CAMPI_POST}}}}}"
    )
    dati = _richiesta(sessione, f"{API}/{ig_user_id}", token, {"fields": campi})
    bd = dati.get("business_discovery") or {}
    return Account(
        username=bd.get("username", username),
        nome=bd.get("name", ""),
        bio=bd.get("biography", ""),
        sito=bd.get("website", ""),
        follower=bd.get("followers_count", 0),
        numero_post=bd.get("media_count", 0),
        post=tuple(_post(m) for m in (bd.get("media") or {}).get("data", [])),
    )


def trova_ig_user_id(*, token: str, sessione=None) -> list[tuple[str, str]]:
    """Pagine Facebook raggiungibili dal token con il loro account Instagram: [(pagina, IG_USER_ID)]."""
    dati = _richiesta(sessione, f"{API}/me/accounts", token, {"fields": "name,instagram_business_account"})
    return [
        (p.get("name", ""), p["instagram_business_account"]["id"])
        for p in dati.get("data", [])
        if p.get("instagram_business_account")
    ]


def _post(m: dict) -> Post:
    return Post(
        id=m.get("id", ""),
        didascalia=m.get("caption", ""),
        like=m.get("like_count"),
        commenti=m.get("comments_count"),
        visualizzazioni=m.get("view_count"),
        tipo=m.get("media_product_type", ""),
        data=m.get("timestamp", ""),
        link=m.get("permalink", ""),
    )


def _richiesta(sessione, url: str, token: str, params: dict) -> dict:
    sessione = sessione or requests
    try:
        risposta = sessione.get(url, params={**params, "access_token": token}, timeout=TIMEOUT)
    except requests.RequestException as errore:
        # Il messaggio originale contiene l'URL con il token: non va mostrato.
        raise ErroreInstagram(f"Meta non raggiungibile ({type(errore).__name__})") from None
    try:
        dati = risposta.json()
    except ValueError:
        raise ErroreInstagram(f"risposta non leggibile da Meta (HTTP {risposta.status_code})") from None
    if "error" in dati or risposta.status_code != 200:
        raise ErroreInstagram(_spiega(dati.get("error") or {}, risposta.status_code))
    return dati


def _spiega(errore: dict, status: int) -> str:
    codice, messaggio = errore.get("code"), errore.get("message", "")
    if codice == 190:
        return f"token non valido o scaduto: rigeneralo seguendo docs/SETUP.md ({messaggio})"
    if codice == 110 or errore.get("error_subcode") == 2207013:
        return f"account non trovato o non professionale (serve un account business o creator) ({messaggio})"
    if codice in (4, 17, 32, 613):
        return f"limite di richieste di Meta raggiunto: riprova più tardi ({messaggio})"
    return f"errore Meta {codice or status}: {messaggio or 'senza dettagli'}"
