import pytest

from config import carica_profilo
from filtri import DA_VERIFICARE, PASSA, SCARTATO, applica_filtri, trova_email
from instagram import Account, Post


def post(tipo="REELS", visualizzazioni=5000, didascalia=""):
    return Post(id="1", didascalia=didascalia, like=100, commenti=10,
                visualizzazioni=visualizzazioni, tipo=tipo, data="", link="")


def account(follower=25000, bio="Contatti: prova@example.com", sito="", posts=None):
    return Account(username="prova", nome="", bio=bio, sito=sito, follower=follower,
                   numero_post=100, post=tuple(posts if posts is not None else [post(), post()]))


@pytest.fixture
def profilo():
    return carica_profilo("it")


def test_passa(profilo):
    esito = applica_filtri(account(), profilo)
    assert esito.esito == PASSA
    assert esito.motivo == "tutti i filtri superati"


def test_follower_sotto_soglia(profilo):
    esito = applica_filtri(account(follower=8000), profilo)
    assert esito.esito == SCARTATO
    assert "8.000" in esito.motivo and "10.000" in esito.motivo


def test_follower_sopra_fascia_di_confronto(profilo):
    esito = applica_filtri(account(follower=350000, posts=[post(visualizzazioni=90000)]), profilo)
    assert esito.esito == SCARTATO
    assert "300.000" in esito.motivo


def test_fascia_di_confronto_passa_con_nota(profilo):
    esito = applica_filtri(account(follower=150000, posts=[post(visualizzazioni=20000)]), profilo)
    assert esito.esito == PASSA
    assert "confronto" in esito.motivo


def test_confini_inclusi(profilo):
    assert applica_filtri(account(follower=10000, posts=[post(visualizzazioni=1000)]), profilo).esito == PASSA
    assert applica_filtri(account(follower=100000, posts=[post(visualizzazioni=10000)]),
                          profilo).motivo == "tutti i filtri superati"


def test_visualizzazioni_reel_basse(profilo):
    posts = [post(visualizzazioni=1000), post(visualizzazioni=2000), post(tipo="FEED", visualizzazioni=None)]
    esito = applica_filtri(account(follower=25000, posts=posts), profilo)
    assert esito.esito == SCARTATO
    assert "1.500" in esito.motivo and "2.500" in esito.motivo


def test_conta_solo_i_reel(profilo):
    posts = [post(visualizzazioni=3000), post(tipo="FEED", visualizzazioni=10)]
    assert applica_filtri(account(posts=posts), profilo).esito == PASSA


def test_nessun_reel_da_verificare(profilo):
    esito = applica_filtri(account(posts=[post(tipo="FEED", visualizzazioni=None)]), profilo)
    assert esito.esito == DA_VERIFICARE
    assert "Reel" in esito.motivo


def test_prodotto_nella_bio_scarta(profilo):
    esito = applica_filtri(account(bio="Scarica il mio ebook! prova@example.com"), profilo)
    assert esito.esito == SCARTATO
    assert "ebook" in esito.motivo and "bio" in esito.motivo


def test_piattaforma_di_vendita_nel_sito_scarta(profilo):
    esito = applica_filtri(account(sito="https://prova.gumroad.com/l/guida"), profilo)
    assert esito.esito == SCARTATO
    assert "gumroad.com" in esito.motivo and "sito" in esito.motivo


def test_prodotto_solo_nelle_didascalie_da_verificare(profilo):
    posts = [post(didascalia="Vi consiglio questo ebook di un'amica"), post()]
    esito = applica_filtri(account(posts=posts), profilo)
    assert esito.esito == DA_VERIFICARE
    assert "didascalie" in esito.motivo


def test_parole_intere(profilo):
    # si cercano parole intere: "workshop online" non contiene "shop online"
    esito = applica_filtri(account(bio="Workshop online gratuiti. prova@example.com"), profilo)
    assert esito.esito == PASSA


def test_email_mancante_da_verificare(profilo):
    esito = applica_filtri(account(bio="Allenamenti a casa"), profilo)
    assert esito.esito == DA_VERIFICARE
    assert "email" in esito.motivo


def test_email_dal_foglio(profilo):
    esito = applica_filtri(account(bio="Allenamenti a casa"), profilo, email="scritta@example.com")
    assert esito.esito == PASSA


def test_scartato_prevale_e_riporta_tutti_i_motivi(profilo):
    esito = applica_filtri(account(follower=5000, bio="Allenamenti"), profilo)
    assert esito.esito == SCARTATO
    assert "follower" in esito.motivo and "email" in esito.motivo
    assert esito.motivo.index("follower") < esito.motivo.index("email")


def test_trova_email():
    assert trova_email("Scrivimi: Nome.Cognome+collab@dominio.it 💌") == "Nome.Cognome+collab@dominio.it"
    assert trova_email("nessuna email qui @utente") == ""
