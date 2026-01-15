# Guida alla Configurazione di Google Sheets

Per utilizzare la funzione di esportazione su Google Spreadsheet, devi configurare un "Service Account" su Google Cloud. È gratis e richiede circa 5 minuti.

## Veloce Riepilogo
Il tuo programma ha bisogno di un "robot" (Service Account) che lo rappresenti per modificare i fogli di calcolo.

## Passaggi Dettagliati

### 1. Crea un Progetto su Google Cloud
1. Vai su [Google Cloud Console](https://console.cloud.google.com/).
2. Clicca sul menu a tendina in alto a sinistra (accanto al logo Google Cloud) e seleziona **"New Project"**.
3. Dai un nome (es. `Text-Analyzer`) e clicca **"Create"**.
4. Seleziona il progetto appena creato.

### 2. Abilita le API Necessarie
1. Nel menu a sinistra, vai su **"APIs & Services" > "Library"**.
2. Cerca **"Google Sheets API"**, cliccaci e premi **"Enable"**.
3. Torna alla Library, cerca **"Google Drive API"**, cliccaci e premi **"Enable"**.

### 3. Crea il Service Account (Il "Robot")
1. Vai su **"APIs & Services" > "Credentials"**.
2. Clicca su **"+ CREATE CREDENTIALS"** (in alto) e scegli **"Service account"**.
3. Dai un nome (es. `analyzer-bot`) e clicca **"Create and Continue"**.
4. (Opzionale) In "Select a role", scegli **"Editor"** (Basic > Editor). Clicca **"Continue"** e poi **"Done"**.

### 4. Scarica la Chiave JSON
1. Nella lista "Service Accounts", clicca sull'indirizzo email del robot appena creato (es. `analyzer-bot@...`).
2. Vai nella tab **"KEYS"** (in alto).
3. Clicca **"ADD KEY" > "Create new key"**.
4. Scegli **JSON** e clicca **"Create"**.
5. Un file verrà scaricato sul tuo computer.

### 5. Configurazione Finale
1. **Rinomina** il file scaricato in `credentials.json`.
2. **Spostalo** nella cartella principale di questo progetto (`Text-Analyzer-CLI/`).
3. **Importante:** Apri il file `credentials.json` e copia l'indirizzo `"client_email"`.
4. Vai sul tuo browser, crea un nuovo foglio Google Sheets (o usane uno esistente).
5. Clicca **"Condividi"** e incolla l'email del robot (`client_email`) dandogli permessi di **Editor**.
6. Copia il **Nome** del foglio (es. "Analisi Text Analyzer").

Ora sei pronto! Quando il programma ti chiederà il nome del foglio, usa quello che hai scelto.
