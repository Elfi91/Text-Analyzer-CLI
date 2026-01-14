# Text-Analyzer-CLI - Specifiche di Prodotto

## 1. Visione del Prodotto
**Obiettivo:** Creare un tool CLI che democratizzi l'uso dell'AI per l'analisi testuale. Il tool deve arricchire dati grezzi (testo) con metadati semantici (sentiment, word count) in modo trasparente, offrendo un'esperienza utente fluida e professionale.

**Valori Chiave:**
*   **Trasparenza:** L'utente non deve preoccuparsi della complessità dell'API di Gemini.
*   **Affidabilità:** I dati vengono salvati localmente e l'applicazione gestisce errori di rete o API con grazia.
*   **Semplicità:** Un singolo comando da terminale per ottenere insights immediati.

## 2. Requisiti Funzionali (User Stories)
### Core (MVP)
*   **Menu Interattivo:** Come utente, voglio un menu interattivo all'avvio che mi permetta di scegliere tra "Analizza Testo", "Vedi Storico" ed "Esci", invece di dover ricordare i comandi flag.
*   **Input Flessibile:** Come utente, voglio poter analizzare una stringa di testo passata direttamente o contenuta in un file.
*   **Analisi Quantitativa:** Come utente, voglio conoscere immediatamente il conteggio di parole, caratteri e righe (calcolato localmente per velocità).
*   **Sentiment Analysis (AI):** Come utente, voglio sapere se il tono del testo è Positivo, Negativo o Neutro e con quale confidenza, grazie all'integrazione con Gemini.
*   **Persistenza Automatica:** Come utente, voglio che ogni mia analisi venga salvata automaticamente in un database locale per poterla consultare in futuro, senza dover esportare nulla manualmente.
*   **Feedback Visivo:** Come utente, voglio vedere uno spinner o una progress bar durante l'attesa dell'analisi AI, per sapere che il sistema sta lavorando.

### Phase 7: Summarization
*   **Riassunto Conciso:** Generare un riassunto di 2-3 frasi del testo analizzato, utile per cogliere il contenuto a colpo d'occhio.

### Future Roadmap
*   **Cronologia:** Visualizzare le ultime 5 analisi effettuate.
*   **Export:** Esportare i risultati in formati standard (Markdown, CSV) e su **Google Spreadsheet**.
*   **Chunking Testi Lunghi:** Dividere documenti molto lunghi (es. libri PDF) in parti più piccole per aggirare limiti di token e filtri di copyright/safety dell'AI.

## 3. Requisiti Non Funzionali
*   **Sicurezza:** Le API Key non devono mai essere esposte nel codice sorgente (uso di `.env`).
*   **Resilienza:** Il sistema deve gestire timeout e *rate limits* delle API con meccanismi di retry o messaggi di errore chiari.
*   **Integrità dei Dati:** Il database non deve corrompersi in caso di chiusura improvvisa o accessi concorrenti (gestione lock).
*   **Usabilità:** I messaggi di errore devono essere "human-readable" e guidare l'utente alla soluzione.

## 4. Architettura Tecnica
Il sistema seguirà il principio della **Separazione delle Responsabilità (SoC)**, diviso in moduli distinti:

### Moduli
1.  **CLI Interface (`cli.py`):** Gestisce l'input utente (argparse), la validazione preliminare e l'output formattato (Rich/print).
2.  **Local Analyzer (`analyzer.py`):** Logica pura per il calcolo delle statistiche locali (word count).
3.  **AI Provider (`ai_client.py`):** Wrapper attorno all'SDK di Gemini. Gestisce l'autenticazione, la costruzione del prompt (Prompt Engineering per output strutturato) e la gestione degli errori API.
4.  **Storage Engine (`storage.py`):** Astrazione sopra TinyDB/JSON. Gestisce salvataggio e recupero dati, inclusi ID univoci e Timestamp.

### Flusso Dati
Input CLI -> Validazione -> Local Stats -> Chiamata AI (Async/Sync) -> Validazione Output AI -> Salvataggio DB -> Output a Video

## 5. Gestione Rischi e Mitigazione
| Rischio | Impatto | Mitigazione |
| :--- | :--- | :--- |
| **Leak API Key** | Critico | `.env` file + `.gitignore`. Controllo pre-commit (opzionale). |
| **Latenza/Timeout API** | Medio | Spinner visivo per UX. Timeout esplicito nella chiamata HTTP. |
| **Output AI non strutturato** | Alto | Prompt Engineering ("Rispondi solo JSON..."). Validazione schema risposta. |
| **Limiti Token/Costi** | Medio | Controllo lunghezza input pre-chiamata (chunking o warning). |
| **Database Locked** | Basso | Uso corretto context managers per I/O su file/DB. |

## 6. Stack Tecnologico
*   **Python:** 3.10+
*   **AI:** `google-generativeai`
*   **DB:** `json` standard (Scelta dettata dalla necessità di nessuna dipendenza esterna per il DB).
*   **CLI:** `argparse` (standard) + `rich` (per UI/Spinner).
*   **Config:** `python-dotenv`.
