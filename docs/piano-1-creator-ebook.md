# Piano 1 — Sistema per trovare creator e creare ebook

Aggiornato: 10 novembre 2026

## Come usare questo piano

- Si lavora una fase alla volta. Durante il lavoro non raccontare i passaggi né i problemi che risolvi da solo.
- A fine fase fermati e riporta solo: cosa non sei riuscito a risolvere, cosa deve fare Manuel, cosa deve verificare.
- Le decisioni sono valide solo per questo progetto. Quelle segnate **DA DECIDERE** si chiedono a Manuel quando servono.
- Segui il CLAUDE.md: niente funzioni oltre il necessario (YAGNI), test prima del codice, file sotto le 500 righe.
- Il portale per i creator è nel piano 2 (`piano-2-portale.md`) e non fa parte di questo lavoro.

## Obiettivo e criterio di successo

Ottenere il primo sì di un creator e la prima vendita di un ebook, con 10-15 minuti al giorno di lavoro di Manuel.

- Classifica delle nicchie pronta e 3 nicchie + 1 esplorativa scelte da Manuel.
- 30-50 creator contattati entro 3 settimane dall'avvio dei contatti.
- Almeno un creator che accetta la collaborazione.
- Primo ebook pubblicato su Whop e almeno una vendita reale.

## Impostazione: codice + sessioni programmate + connettori

Niente server e niente bot per partire. Il sistema ha tre parti:

- **Codice (Python, nel repository, con test):** le parti meccaniche. Dati da Instagram, filtri, lettura e scrittura del foglio, calcolo dei promemoria, riepilogo.
- **Claude nella sessione:** le parti di ragionamento. Punteggio delle nicchie, analisi dei creator, testi dei messaggi, classificazione delle risposte, ebook.
- **Connettori:** gli account. Bozze in Gmail, file su Drive.

Un'attività programmata di Claude Code avvia il lavoro una o due volte al giorno e manda a Manuel una notifica con il riepilogo. Manuel aggiunge i creator nel foglio e invia le bozze dall'app di Gmail.

### Regole per poter passare a un server in seguito

1. Le istruzioni per Claude (analisi del creator, messaggio, classificazione delle risposte, punteggio delle nicchie) stanno in file nel repository, in `prompts/`, non dentro il testo dell'attività programmata.
2. Ogni collegamento esterno sta in un modulo separato con un'interfaccia semplice (per esempio `crea_bozza_email`), così la versione con connettore si sostituisce con quella via API cambiando solo quel modulo.
3. Il Foglio Google è l'unica fonte dei dati su creator e contatti. I dati personali non vanno mai nel repository.

Si passa a un server (VPS, cron, API di Claude, credenziali Google proprie, eventuale bot Telegram) solo se i creator superano i limiti del piano di Manuel o servono risposte in tempo reale.

## Decisioni

| Decisione | Scelta |
| --- | --- |
| Esecuzione | Attività programmate di Claude Code in cloud, 1-2 volte al giorno |
| Linguaggio | Python, tutto in un solo repository |
| Dati con informazioni personali | Foglio Google con le schede Creator e Contatti |
| Dati senza informazioni personali | Classifica delle nicchie come CSV nel repository (`data/nicchie.csv`), con la sua cronologia |
| Accesso al foglio dal codice | Account di servizio Google |
| Email | Google Workspace su un dominio dedicato, bozze create in Gmail |
| Dominio | Uno solo per questa attività, separato dalla consulenza |
| Mercati | Italiano e inglese |
| Dati sui volumi di ricerca | Facoltativi, DataForSEO a consumo — **DA DECIDERE** in fase 1 |
| Trascrizione dei vocali | **DA DECIDERE** prima della fase ebook |
| Nome con cui Manuel si presenta | **DA DECIDERE** prima della fase 3 (serve per il dominio) |
| Account Google per fasi 0-2 | Quello attuale di Manuel; si passa a Workspace prima della fase 3 |

## Passaggi del sistema

1. Trovare le nicchie più promettenti (punteggio sotto).
2. Trovare i creator in quelle nicchie, con i filtri.
3. Controllo web veloce su chi passa i filtri, poi bozze dei messaggi basate sui loro profili.
4. Manuel invia le bozze; il sistema gestisce promemoria e risposte.
5. Approfondimento con ricerca web sui creator che rispondono con interesse.
6. Accordo con il creator che dice sì.
7. Scelta del tema con il creator e intervista.
8. Creazione dell'ebook, rivisto e approvato dal creator.
9. Pubblicazione su Whop, con divisione dei ricavi e vendita di prova.
10. Kit di lancio per il creator e monitoraggio delle vendite.

Controllo veloce (passaggio 3): pochi minuti per creator. Cerca altri canali (YouTube, TikTok, sito, newsletter) e prodotti già in vendita fuori da Instagram (pagine di link, negozi come Gumroad o Stan, corsi), così il filtro "nessun prodotto proprio" è affidabile e il messaggio è più preciso.

Approfondimento (passaggio 5): solo per chi risponde con interesse. Pubblico sui vari canali, temi che funzionano meglio, collaborazioni e sponsor, prodotti passati. Serve a preparare la chiamata e l'accordo.

## Punteggio delle nicchie

Il punteggio stima quanto rende ogni ora di lavoro in una nicchia: creator disponibili → dicono sì → il pubblico compra → compra di nuovo. Sono pesi di partenza: si ritarano dopo le prime classifiche e dopo il test.

### Due livelli di nicchia

1. **Nicchia per cercare i creator (chi + tema).** Esempio: "neomamme che vogliono tornare in forma". Deve avere almeno 20 creator nel mercato italiano e 50 in quello inglese che passano i filtri. Il punteggio si dà a questo livello.
2. **Angolo del prodotto (chi + problema + momento + risultato).** Esempio: "12 settimane, 20 minuti al giorno, senza attrezzi, nel primo anno dopo il parto". Si decide dopo, con il creator e i dati del suo pubblico.

Prove per il livello giusto: la persona si riconosce in una frase, il titolo può promettere un risultato concreto, ci sono abbastanza creator.

### Esclusioni

Si scartano senza punteggio:

- investimenti, trading, crypto;
- cure mediche, integratori con promesse, dimagrimento rapido, diete estreme;
- gioco d'azzardo, contenuti per adulti;
- pubblico in prevalenza minorenne;
- "guadagnare online".

### Criteri

Ogni criterio riceve un voto da 1 a 5, con le prove (link) che lo giustificano.

| Criterio | Peso | Come si misura | Voto 5 | Voto 1 |
| --- | --- | --- | --- | --- |
| Disponibilità a pagare | 25 | Prodotti a pagamento sul tema con acquisti recenti: recensioni degli ultimi 6-12 mesi, prodotti nuovi che vendono | Molti prodotti con recensioni recenti, prezzi sopra i 20 € | Quasi nessun prodotto, o solo recensioni vecchie |
| Urgenza del problema | 15 | Quanto costa non risolverlo: tempo, soldi, salute, relazioni | Problema concreto, sentito ogni giorno | Curiosità o intrattenimento |
| Creator disponibili | 15 | Su un campione di 30 profili della nicchia, quanti passano i filtri | Più di uno su tre | Meno di uno su dieci |
| Durata del bisogno | 10 | Per quanto tempo serve una guida (conta per l'abbonamento) | Anni | Pochi giorni (3 = una fase di mesi: matrimonio, gravidanza, esame) |
| Ricambio del pubblico | 10 | Quante persone nuove entrano ogni mese in quella situazione (conta per l'ebook) | Ricambio continuo: nuove coppie, neogenitori, studenti | Pubblico fisso che non si rinnova |
| Potere d'acquisto | 10 | Età e situazione tipiche del pubblico | Adulti con reddito che già spendono per quel problema | Pubblico giovane o senza capacità di spesa |
| Fattibilità del prodotto | 10 | Prodotto utile in 30-60 pagine con il sapere del creator e fonti pubbliche | Sapere pratico e stabile | Servono competenze certificate o cambia ogni mese |
| Concorrenza nel segmento | 5 | Prodotti simili nella stessa lingua e nello stesso segmento, lacune nelle recensioni | Concorrenza moderata, con bisogni scoperti | Nessun prodotto (manca la domanda) o segmento saturo |

### Calcolo

- Base = somma di (peso × voto) ÷ 5, da 20 a 100.
- Finale = base × moltiplicatore di rischio:
    - 1,0 basso: cucina, organizzazione, lingue, hobby;
    - 0,8 medio: fitness generale, genitori, relazioni (servono avvertenze);
    - 0,6 alto: alimentazione legata a condizioni di salute, benessere psicologico (il creator deve essere un professionista qualificato).
- Punteggio separato per mercato italiano e inglese.

### Affidabilità

- Ogni criterio con meno di 3 prove rende il punteggio "poco affidabile": la nicchia non si scarta, si prova con pochi contatti.
- Ogni nicchia si valuta due volte e si fa la media, perché i voti di Claude possono variare tra esecuzioni.

### Uso e ritaratura

- Manuel controlla a mano le prime 10 della classifica e annota perché una nicchia non ha senso: il motivo indica quale peso correggere.
- Nel test: le prime 3 nicchie più 1 esplorativa (punteggio incerto, buon potenziale), circa 10 creator ciascuna.
- Dopo il test: confronto tra punteggio previsto e risultati reali per nicchia (risposte, sì, vendite) e correzione dei pesi.
- Classifica aggiornata una volta al mese.

## Filtri dei creator

Soglie di partenza, in un file di profilo per mercato (lingua, tono, soglie, prezzi indicativi):

- follower tra 10.000 e 100.000, più alcuni tra 100.000 e 300.000 per confronto;
- visualizzazioni medie dei Reel almeno pari a un decimo dei follower;
- nessun prodotto proprio in vendita (bio, link, didascalie);
- email business presente.

Dati dall'API ufficiale di Instagram (Business Discovery): follower, post, like, commenti, visualizzazioni, bio, sito. Manuel aggiunge i nomi utente nel foglio mentre scorre Esplora.

## Fasi

1. **Fase 0 — Preparazione e verifica.**
    - Manuel (1-2 ore), seguendo `docs/SETUP.md`: foglio Google e account di servizio sul suo account Google attuale, account Instagram professionale collegato a una pagina Facebook, app Meta per sviluppatori e token, collegamento di Gmail e Drive a Claude, segreti e domini nell'ambiente cloud. Dominio e Workspace servono dalla fase 3, l'account Whop dalla fase 7.
    - Claude Code: repository, struttura dei moduli, segreti e domini dell'ambiente cloud, attività programmata di prova.
    - Fatto quando: un'esecuzione programmata di prova legge il foglio, crea una bozza in Gmail e una richiesta all'API di Instagram restituisce i dati di un creator.
2. **Fase 1 — Analisi delle nicchie.** Istruzioni in `prompts/`, `data/nicchie.csv` con voti, prove e punteggio per mercato. Fatto quando: Manuel ha controllato le prime 10 e scelto 3 nicchie + 1 esplorativa.
3. **Fase 2 — Creator e filtri.** Fatto quando: 10 nomi utente aggiunti nel foglio compaiono con dati e filtri corretti (Manuel ne controlla 3 a mano).
4. **Fase 3 — Controllo web, analisi e bozze.** Prima di iniziare: nome, dominio dedicato e Google Workspace; il foglio si copia nel Drive di Workspace (nuovo `SHEET_ID`, condiviso con l'account di servizio) e Gmail si ricollega all'account nuovo. Bozze personalizzate in italiano o inglese, con un riferimento a 1-2 contenuti del creator, create in Gmail. Fatto quando: per 10 creator ci sono le bozze in Gmail e il foglio è aggiornato.
5. **Fase 4 — Risposte e promemoria.** Il sistema legge le risposte, le classifica (sì, forse, no, richiesta di informazioni), aggiorna il foglio e prepara le bozze di replica. Promemoria dopo 4-5 giorni, al massimo due; stop se il creator risponde o chiede di non essere ricontattato. Notifica serale con il riepilogo. Fatto quando: il ciclo funziona con una casella di prova di Manuel.
6. **STOP — Test reale.** 30-50 creator in 2-3 settimane. Se non arriva nessun sì si cambiano messaggio, nicchie o fasce di follower; non si costruisce altro finché i contatti non funzionano.
7. **Fase 5 — Ebook.** Dopo il primo sì, in sessione con Manuel. Didascalie dall'API, video e vocali dal creator, 3-5 temi proposti, domande per l'intervista, trascrizione, ricerca delle fonti, indice, capitoli con la scheda di stile, controlli (fatti sulle fonti, passaggi copiati, coerenza dello stile). Fatto quando: Manuel ha letto la bozza e il creator l'ha approvata.
8. **Fase 6 — PDF e kit di lancio.** PDF con la grafica del creator; pagina di vendita per Whop, script per le storie, didascalie, email per la lista del creator.
9. **Fase 7 — Whop e prima vendita.** Prodotto online, divisione dei ricavi attiva, vendita di prova da pochi euro; il riepilogo generato da Whop va al commercialista.

## Modello consigliato per fase

Il modello si sceglie nella sessione prima di incollare il prompt. Se un passaggio si blocca su un problema difficile, si alza lo sforzo solo per quel passaggio.

| Fase | Modello | Sforzo |
| --- | --- | --- |
| 0 — Preparazione e verifica | Opus | Alto |
| 1 — Analisi delle nicchie | Opus | Alto |
| 2 — Creator e filtri | Sonnet | Normale |
| 3 — Analisi e bozze (sviluppo) | Sonnet | Normale |
| 4 — Risposte e promemoria | Sonnet | Normale |
| Attività programmate di ogni giorno | Sonnet | Normale |
| 5 — Ebook | Opus | Alto |
| 6 — PDF e kit di lancio | Sonnet | Normale |
| 7 — Whop e prima vendita | Sonnet | Normale |

## Domini di rete da autorizzare nell'ambiente cloud

| Dominio | A cosa serve | Fase |
| --- | --- | --- |
| graph.facebook.com | Dati Instagram (Business Discovery) | 0 |
| oauth2.googleapis.com, sheets.googleapis.com | Foglio, se l'accesso è dal codice | 0 |
| api.dataforseo.com | Volumi di ricerca, solo se scelti | 1 |
| Dominio del servizio di trascrizione scelto | Trascrizione dei vocali | 5 |
| api.whop.com | Solo se si automatizza Whop | 7 |
| pypi.org, files.pythonhosted.org, github.com | Pacchetti e codice | Tutte |

Ricerche web, Gmail e Drive passano dagli strumenti e dai connettori di Claude, non dal codice. Playwright scarica i browser da domini propri alla prima installazione: segnalali a Manuel in quel momento.

## Costi

| Voce | Costo | Note |
| --- | --- | --- |
| Google Workspace | 6,80 € al mese con impegno annuale, 8,10 € con pagamento mensile | |
| Dominio | Circa 10-20 € l'anno | |
| Claude | Abbonamento di Manuel | Le attività programmate consumano i limiti del piano |
| API di Instagram | Nessun costo per richiesta indicato da Meta | |
| DataForSEO | Pochi centesimi a richiesta | Facoltativo |
| Trascrizione | A consumo | Solo dalla fase 5 |
| Whop | Commissione su ogni vendita | Nessun costo fisso |

## Regole e vincoli

- **Instagram:** niente messaggi privati automatici, niente raccolta di dati fuori dall'API ufficiale. Il primo contatto passa dall'email.
- **Email:** le invia Manuel, una per una, personalizzate e con un modo semplice per non essere più contattati. Per aumentare i volumi serve prima il parere di un professionista sulle regole italiane ed europee.
- **Segreti:** token e credenziali solo nei segreti dell'ambiente, mai nel repository.
- **Attività programmate:** impostate in modo da non fermarsi in attesa di approvazioni durante l'esecuzione.
- **Contenuti:** l'ebook rielabora e cita le fonti, senza copiarne interi passaggi.
- **Temi delicati:** salute, soldi e bambini richiedono la revisione dell'esperto.
- **Approvazione:** il creator approva tutto prima della pubblicazione.
- **Fisco:** partita IVA aperta prima di incassare.

## Quando passare al piano 2

Solo quando valgono tutte e tre:

1. Un creator ha venduto l'ebook, quindi il suo pubblico ha dimostrato di comprare.
2. Il creator vuole un abbonamento e si impegna a pubblicare contenuti nuovi ogni mese.
3. Il piano 1 gira con meno di 15 minuti al giorno del tempo di Manuel.

## Note non tecniche: accordo con il creator

Non riguarda lo sviluppo. Punti dell'accordo scritto, da far rivedere a un avvocato:

- Promozione minima: link fisso nella bio, storie a ogni lancio, una menzione al mese, newsletter se c'è.
- Divisione 50/50 al netto delle commissioni Whop e dei rimborsi, pagata in automatico da Whop.
- Il prodotto si vende dall'account Whop di Manuel, con il creator come socio nella divisione dei ricavi.
- Chi risponde ai clienti, chi gestisce i rimborsi, chi aggiorna il prodotto.
- Approvazione del creator su ogni versione.
- Proprietà del prodotto e cosa succede se uno dei due chiude la collaborazione.
- Come si rivede l'accordo se il creator cresce molto.
