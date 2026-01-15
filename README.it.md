# 🔍 Text-Analyzer-CLI

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![🇬🇧 Read in English](https://img.shields.io/badge/Lang-English-blue)](README.md)

**Text-Analyzer-CLI** è un potente strumento da riga di comando che sfrutta **Google Gemini AI** per analizzare file di testo (TXT, PDF), fornendo insight approfonditi, analisi del sentiment e riassunti concisi.

## ✨ Funzionalità

- **📄 Supporto Testo & PDF**: Analizza stringhe di testo grezzo o interi file (supporta `.txt` e `.pdf` con estrazione del testo).
- **🧠 Analisi AI**:
    - **Sentiment Analysis**: Rileva il tono (Positivo, Negativo, Neutro) con un punteggio di confidenza.
    - **AI Summarization**: Genera un riassunto di 2-3 frasi del contenuto analizzato.
- **📊 Statistiche Locali**: Calcolo istantaneo di numero parole, caratteri e righe.
- **💾 Database Locale**: Salvataggio automatico di ogni analisi in un database JSON locale (`data/db.json`).
- **📜 Storico & Persistenza**: Visualizza lo storico delle analisi direttamente dal terminale.
- **📤 Esportazione Dati**:
    - **CSV**: Esporta lo storico per fogli di calcolo.
    - **Markdown**: Genera report leggibili.
    - **Google Sheets**: Carica direttamente i dati sul cloud (Google Fogli).

## 📂 Struttura del Progetto

```bash
Text-Analyzer-CLI/
├── data/
│   └── db.json                # Database JSON per lo storico analisi
├── docs/
│   ├── GOOGLE_SETUP.md        # Guida per il setup di Google Sheets
│   └── specifications.md      # Specifiche del progetto
├── exports/                   # Cartella per i file esportati (CSV, MD)
├── logs/
│   └── app.log                # Log dell'applicazione
├── scripts/
│   ├── list_models.py         # Script per elencare i modelli Gemini disponibili
│   └── verify_gemini.py       # Script per verificare la connessione alle API Gemini
├── src/
│   ├── ai_client.py           # Logica di integrazione con Gemini AI
│   ├── analyzer.py            # Logica di analisi locale del testo (statistiche)
│   ├── exporter.py            # Logica per l'esportazione dei dati (CSV, MD, Sheets)
│   ├── main.py                # Punto di ingresso principale e interfaccia CLI
│   ├── pdf_utils.py           # Utilità per la gestione dei file PDF
│   └── storage.py             # Gestione dell'archiviazione JSON
├── tests/
│   ├── test_analyzer.py       # Test per l'analisi locale
│   └── test_storage.py        # Test per le operazioni di storage
├── .env                       # Variabili d'ambiente (API Keys)
├── .gitignore                 # Regole per git ignore
├── credentials.json           # Chiave Google Service Account (ignorato da git)
├── LICENSE                    # File di licenza
├── README.md                  # Documentazione del progetto (Inglese)
├── README.it.md               # Documentazione del progetto (Italiano)
└── requirements.txt           # Dipendenze Python
```

## 🚀 Guida Rapida

### 1. Installazione

```bash
# Clona il repository
git clone https://github.com/Elfi91/Text-Analyzer-CLI.git
cd Text-Analyzer-CLI

# Crea l'ambiente virtuale
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Installa le dipendenze
pip install -r requirements.txt
```

### 2. Configurazione

1. Crea un file `.env` nella directory principale:
   ```bash
   cp .env.example .env
   ```
2. Aggiungi la tua **Google Gemini API Key** nel file `.env`:
   ```env
   GEMINI_API_KEY=la_tua_chiave_api_qui
   ```
3. *(Opzionale)* Per l'export su Google Sheets, posiziona il file `credentials.json` nella cartella principale (vedi [docs/GOOGLE_SETUP.md](docs/GOOGLE_SETUP.md)).

### 3. Utilizzo

**Modalità Interattiva (Consigliata):**
```bash
python src/main.py
```
Segui il menu a schermo per analizzare file, vedere lo storico o esportare i dati.

**Modalità Comando Diretto:**
```bash
# Analizza una stringa di testo
python src/main.py --text "Adoro questo prodotto!"

# Analizza un file
python src/main.py --file percorso/del/documento.pdf
```

## 🧪 Eseguire i Test

Per verificare la logica di base:
```bash
pytest tests/
```

## 🔒 Nota sulla Sicurezza

- **API Keys**: Salvate nel file `.env` (ignorato da Git).
- **Google Credentials**: `credentials.json` è ignorato da Git.
- **Log**: I log di sistema in `logs/` sono ignorati da Git.
