# Configurazione della fase 0

Guida passo passo per Manuel. Tempo totale: 1-2 ore.

- 💻 = conviene farlo da computer (console con molti menu, file da scaricare, testo lungo da copiare).
- 📱 = va bene anche dal telefono.

Le voci dei menu di Google e Meta cambiano spesso nome o posizione: se non trovi una voce identica, cerca quella con il significato più vicino.

Alla fine avrai quattro valori, da inserire **solo** nelle impostazioni dell'ambiente cloud (passo 5), mai nel repository, in chat o per email:

| Variabile | Cos'è |
| --- | --- |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Il contenuto del file JSON dell'account di servizio Google, su una riga |
| `SHEET_ID` | L'identificativo del Foglio Google |
| `IG_ACCESS_TOKEN` | Il token di Meta che non scade |
| `IG_USER_ID` | L'ID del tuo account Instagram professionale (cifre) |

---

## 1. Foglio Google e account di servizio (account Google attuale)

### 1.1 Crea il foglio 📱

1. Apri [sheets.google.com](https://sheets.google.com) e crea un foglio vuoto. Chiamalo per esempio `Sistema creator`.
2. Non creare schede né colonne: le crea `scripts/verifica.py` (schede **Creator** e **Contatti**).
3. Copia l'indirizzo del foglio. Ha questa forma:
   `https://docs.google.com/spreadsheets/d/QUESTO_È_LO_SHEET_ID/edit`
   La parte tra `/d/` e `/edit` è il **`SHEET_ID`**.

### 1.2 Crea il progetto e attiva l'API 💻

1. Apri [console.cloud.google.com](https://console.cloud.google.com) con lo stesso account Google e accetta i termini.
2. In alto, selettore dei progetti → **Nuovo progetto** → nome `sistema-creator` → **Crea**. Non serve un account di fatturazione.
3. Con il progetto selezionato: menu ☰ → **API e servizi** → **Libreria** → cerca **Google Sheets API** → **Abilita**.

### 1.3 Crea l'account di servizio e la chiave 💻

1. Menu ☰ → **IAM e amministrazione** → **Account di servizio** → **Crea account di servizio**.
2. Nome `sistema-creator` → **Crea e continua**. Salta i ruoli (non servono) → **Fine**.
3. Apri l'account appena creato → scheda **Chiavi** → **Aggiungi chiave** → **Crea nuova chiave** → **JSON** → **Crea**. Il computer scarica un file `.json`.
4. Questo file è una password: non mandarlo per email, non caricarlo su Drive o nel repository.
5. Nella pagina dell'account di servizio copia l'**email**, che finisce con `.iam.gserviceaccount.com`.

### 1.4 Condividi il foglio con l'account di servizio 📱

1. Nel foglio: **Condividi** → incolla l'email dell'account di servizio.
2. Ruolo **Editor**, togli la spunta da **Invia notifica** → **Condividi**.

L'account di servizio vede solo i file condivisi con lui: se il codice dovesse finire in mani sbagliate, si arriva solo a questo foglio.

### 1.5 Prepara il JSON su una riga 💻

Le variabili d'ambiente stanno su una riga sola, il file JSON no. Unisci le righe senza usare siti esterni:

- **Mac** (app Terminale), nella cartella dove hai scaricato il file:
  `tr -d '\n' < nome-del-file.json | pbcopy`
- **Windows** (PowerShell):
  `(Get-Content nome-del-file.json -Raw) -replace "\r?\n","" | Set-Clipboard`

Ora il JSON su una riga è negli appunti: tienilo pronto per il passo 5. Dopo averlo inserito, cancella il file dai Download e svuota il cestino.

---

## 2. Instagram professionale e pagina Facebook 📱

1. **Account professionale.** App Instagram → profilo → ☰ → **Tipo di account e strumenti** (o **Strumenti per professionisti**) → **Passa a un account professionale** → **Azienda** o **Creator** (vanno bene entrambi). Puoi usare un account nuovo dedicato a questa attività: il nome si può cambiare dopo.
2. **Pagina Facebook.** App Facebook → ☰ → **Pagine** → **Crea**. Basta un nome e una categoria.
3. **Collegamento.** In Instagram: **Modifica profilo** → **Pagina** → **Collega** e scegli la pagina appena creata. In alternativa da [business.facebook.com](https://business.facebook.com) → **Impostazioni** → **Account Instagram** → **Collega**.

L'account Instagram usato per le richieste resta invisibile ai creator: Business Discovery legge solo dati pubblici e non manda notifiche.

---

## 3. Portfolio business, app Meta e token che non scade 💻

### 3.1 Portfolio business

1. Apri [business.facebook.com](https://business.facebook.com) e crea un portfolio business (Meta Business Suite), se non ne hai già uno.
2. **Impostazioni** → **Account** → **Pagine**: aggiungi la pagina del passo 2. **Account Instagram**: aggiungi l'account del passo 2.

### 3.2 App Meta per sviluppatori

1. Apri [developers.facebook.com](https://developers.facebook.com) → **Inizia** e registrati come sviluppatore (chiede la verifica del telefono).
2. **Le mie app** → **Crea app**.
3. Quando chiede il caso d'uso scegli **Altro**, poi il tipo **Business**. Nome `sistema-creator`. Collega l'app al portfolio business del passo 3.1.
4. Nella dashboard dell'app aggiungi il prodotto **Instagram** e scegli **API setup with Facebook login** (configurazione con accesso tramite Facebook). Non scegliere la configurazione "con accesso tramite Instagram": quella non permette Business Discovery.
5. L'app può restare in **modalità sviluppo**: serve solo al tuo account, quindi basta l'accesso standard e non serve la revisione di Meta.

### 3.3 Token che non scade (utente di sistema)

Un normale token utente dura 60 giorni. Il token di un **utente di sistema** può non scadere mai.

1. [business.facebook.com](https://business.facebook.com) → **Impostazioni** → **Utenti** → **Utenti di sistema** → **Aggiungi**. Nome `sistema-creator`, ruolo **Amministratore**.
2. Selezionalo → **Assegna risorse**:
   - **App** → `sistema-creator` → controllo completo;
   - **Pagine** → la tua pagina → controllo completo;
   - **Account Instagram** → il tuo account → controllo completo.
3. **Genera nuovo token** → scegli l'app `sistema-creator` → scadenza **Mai**.
4. Seleziona queste autorizzazioni:
   - `instagram_basic`
   - `instagram_manage_insights`
   - `pages_read_engagement`
   - `pages_show_list`
   - `business_management`
   - `ads_read` (Meta la richiede quando la pagina è gestita tramite un portfolio business)
5. **Genera token** e copialo subito: Meta lo mostra una volta sola. È il tuo **`IG_ACCESS_TOKEN`**. Tienilo pronto per il passo 5.

**Se l'utente di sistema non funziona** (lo script del passo 6 dice "token non valido"), usa un token utente da 60 giorni: [Graph API Explorer](https://developers.facebook.com/tools/explorer) → app `sistema-creator` → **Genera token di accesso** con le stesse autorizzazioni → icona ⓘ → **Apri in Strumento token di accesso** → **Estendi token di accesso**. Segnati in calendario di rigenerarlo dopo 50 giorni.

### 3.4 ID dell'account Instagram

Il modo più semplice: lascia `IG_USER_ID` vuoto e avvia lo script del passo 6. Se manca, lo script elenca le pagine che il token vede e stampa l'`IG_USER_ID` accanto a ciascuna. Copialo e aggiungilo alle variabili.

In alternativa, da [Graph API Explorer](https://developers.facebook.com/tools/explorer) con il token: richiesta `me/accounts?fields=name,instagram_business_account`. L'ID è il valore `id` dentro `instagram_business_account` (sono solo cifre e inizia di solito con `1784`).

---

## 4. Connettori Gmail e Drive in Claude 📱

1. Apri [claude.ai/customize/connectors](https://claude.ai/customize/connectors) (dall'app: **Impostazioni** → **Connettori**).
2. Collega **Gmail** e **Google Drive** con l'account Google attuale.
3. I connettori si leggono all'avvio della sessione: dopo averli collegati, apri una **sessione nuova**.

Prima della fase 3 colleghi Gmail all'account Workspace del dominio dedicato al posto di questo.

---

## 5. Segreti nell'ambiente cloud `sistema-creator` 💻

L'ambiente `sistema-creator` esiste già ed è personale. È configurato così:

- **Rete limitata:** raggiunge `graph.facebook.com`, `oauth2.googleapis.com`, `sheets.googleapis.com`, `github.com` e i gestori di pacchetti (pypi).
- **Script di preparazione:** installa i pacchetti Python del repository all'avvio di ogni sessione.
- **Repository:** `sistema-creator` è collegato.

Manca solo una cosa: i segreti. Conviene farlo da computer, dove hai negli appunti il JSON del passo 1.5.

1. In una sessione di Claude Code sul web: menu dell'ambiente nella barra del titolo → **Modifica** su `sistema-creator`.
2. In **Variabili d'ambiente** scrivi una variabile per riga, senza virgolette:
   ```
   GOOGLE_SERVICE_ACCOUNT_JSON={"type": "service_account", ... tutto il JSON su una riga ...}
   SHEET_ID=...
   IG_ACCESS_TOKEN=...
   IG_USER_ID=...
   ```
   Se non hai ancora `IG_USER_ID`, togli quella riga: te lo trova lo script del passo 6 (vedi passo 3.4).
3. Salva. Le variabili si leggono all'avvio della sessione: apri una **sessione nuova** su `sistema-creator`.

Le variabili sono visibili a chi può modificare l'ambiente: lascialo **personale**.

Le attività programmate useranno lo stesso ambiente: quando le creeremo, scegli `sistema-creator`.

---

## 6. Verifica 📱

In una sessione nuova sull'ambiente `sistema-creator` chiedi a Claude:

> Esegui `python scripts/verifica.py NOME_UTENTE` con il nome di un creator con account professionale.

Lo script:

1. legge il foglio, crea le schede **Creator** e **Contatti** con le intestazioni se mancano;
2. scrive una riga di prova nella scheda **Contatti** (`prova_verifica`: poi puoi cancellarla);
3. chiama Business Discovery sul nome utente e mostra follower, post, Reel letti ed esito dei filtri.

Per il mercato inglese aggiungi `--mercato en`.

| Messaggio | Cosa fare |
| --- | --- |
| `Manca la variabile d'ambiente ...` | Aggiungila al passo 5 e apri una sessione nuova |
| `accesso negato: il foglio non è condiviso` | Ripeti il passo 1.4 con l'email esatta dell'account di servizio |
| `foglio non trovato` | Ricontrolla `SHEET_ID` (passo 1.1) |
| `GOOGLE_SERVICE_ACCOUNT_JSON non è un JSON valido` | Ripeti il passo 1.5 e reincolla il JSON intero |
| `token non valido o scaduto` | Rigenera il token (passo 3.3) |
| `account non trovato o non professionale` | Il nome utente non esiste o non è un account professionale: provane un altro |
| `Meta non raggiungibile` | Controlla che la sessione usi l'ambiente `sistema-creator` (passo 5) |

La fase 0 è chiusa quando la verifica passa e un'attività programmata di prova legge il foglio e crea una bozza in Gmail.
