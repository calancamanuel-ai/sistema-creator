import pytest
from conftest import RispostaFinta, SessioneFinta

from instagram import ErroreInstagram, dati_account, trova_ig_user_id


def chiama(risposta, username="profilo_prova", **kwargs):
    sessione = SessioneFinta([risposta])
    account = dati_account(username, token="TOKEN", ig_user_id="1784", sessione=sessione, **kwargs)
    return account, sessione


def test_legge_account_e_post(business_discovery):
    account, _ = chiama(RispostaFinta(200, business_discovery))
    assert account.username == "profilo_prova"
    assert account.nome == "Profilo di Prova"
    assert "neomamme" in account.bio
    assert account.sito == "https://example.com"
    assert account.follower == 25000
    assert account.numero_post == 340
    assert len(account.post) == 3
    reel = account.post[0]
    assert (reel.like, reel.commenti, reel.visualizzazioni) == (1200, 85, 4000)
    assert reel.tipo == "REELS"
    assert reel.didascalia.startswith("Circuito")
    assert reel.link == "https://www.instagram.com/reel/AAA/"


def test_campi_mancanti_diventano_none_o_vuoti(business_discovery):
    account, _ = chiama(RispostaFinta(200, business_discovery))
    carosello, reel_senza_didascalia = account.post[1], account.post[2]
    assert carosello.like is None  # like nascosti dal creator
    assert carosello.visualizzazioni is None
    assert reel_senza_didascalia.didascalia == ""


def test_richiesta_corretta(business_discovery):
    _, sessione = chiama(RispostaFinta(200, business_discovery), username="@Profilo_Prova", n_post=5)
    chiamata = sessione.chiamate[0]
    assert chiamata["url"].startswith("https://graph.facebook.com/v")
    assert chiamata["url"].endswith("/1784")
    campi = chiamata["params"]["fields"]
    assert campi.startswith("business_discovery.username(Profilo_Prova)")
    for campo in ["followers_count", "media_count", "biography", "website",
                  "media.limit(5)", "like_count", "comments_count", "view_count", "caption"]:
        assert campo in campi
    assert chiamata["params"]["access_token"] == "TOKEN"
    assert "TOKEN" not in chiamata["url"]


def test_errore_di_rete_non_mostra_il_token():
    import requests

    class SessioneSenzaRete(SessioneFinta):
        def get(self, url, **kwargs):
            raise requests.ConnectionError(f"impossibile aprire {url}?access_token={kwargs['params']['access_token']}")

    with pytest.raises(ErroreInstagram) as errore:
        dati_account("ok", token="SEGRETO", ig_user_id="1", sessione=SessioneSenzaRete())
    assert "SEGRETO" not in str(errore.value)


def test_account_senza_post():
    dati = {"business_discovery": {"username": "vuoto", "followers_count": 10, "media_count": 0}}
    account, _ = chiama(RispostaFinta(200, dati), username="vuoto")
    assert account.post == ()
    assert account.bio == "" and account.sito == ""


@pytest.mark.parametrize("username", ["", "nome con spazi", "a" * 31, "x){id}", "nome/altro"])
def test_nome_utente_non_valido(username):
    with pytest.raises(ValueError):
        dati_account(username, token="T", ig_user_id="1", sessione=SessioneFinta())


def test_ig_user_id_non_valido():
    with pytest.raises(ValueError):
        dati_account("ok", token="T", ig_user_id="abc", sessione=SessioneFinta())


@pytest.mark.parametrize(
    "errore, testo",
    [
        ({"code": 190, "message": "Error validating access token"}, "token"),
        ({"code": 110, "error_subcode": 2207013, "message": "Invalid user id"}, "professionale"),
        ({"code": 4, "message": "Application request limit reached"}, "limite"),
        ({"code": 100, "message": "Unsupported get request"}, "Unsupported get request"),
    ],
)
def test_errori_meta_tradotti(errore, testo):
    with pytest.raises(ErroreInstagram, match=testo):
        chiama(RispostaFinta(400, {"error": errore}))


def test_risposta_non_json():
    with pytest.raises(ErroreInstagram, match="non leggibile"):
        chiama(RispostaFinta(502, ValueError("no json")))


def test_trova_ig_user_id():
    dati = {"data": [
        {"name": "Pagina A", "id": "1", "instagram_business_account": {"id": "1784A"}},
        {"name": "Pagina senza IG", "id": "2"},
    ]}
    sessione = SessioneFinta([RispostaFinta(200, dati)])
    assert trova_ig_user_id(token="TOKEN", sessione=sessione) == [("Pagina A", "1784A")]
    chiamata = sessione.chiamate[0]
    assert chiamata["url"].endswith("/me/accounts")
    assert chiamata["params"]["access_token"] == "TOKEN"
