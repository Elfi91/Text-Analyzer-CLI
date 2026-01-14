# Text-Analyzer-CLI
Specifiche Tecniche del Progetto

Tool CLI che analizza un testo tramite le API di Gemini (sentiment analysis + word count) e salva l'output su DB.

**Obiettivo**

- Automazione dell'insight: Dimostrare come l'AI possa arricchire dati grezzi (il testo) con metadati semantici (sentiment, word count) in modo trasparente per l'utente.
- User Experience CLI: Fornire un'interfaccia a riga di comando fluida e intuitiva, con messaggi di stato chiari (es. in corso, completato, errore) e feedback visivi (es. spinner o progress bar).
- Integrità dei dati: Assicurare che i dati siano salvati e archiviati in modo corretto e in modo trasparente per l'utente, garantendo la persistenza anche dopo un crash o un riavvio del sistema.
- Separazione delle responsabilità: Scrivere codice modulare dove la logica di calcolo locale, la chiamata all'API, l'accesso al DB e la persistenza dei dati siano separate in moduli distinti.

**Possibili problemi**
1. Gestione delle API Key e Sicurezza:
- Problema: Caricare per errore la chiave Gemini su GitHub.
- Soluzione: Caricare la API Key da un file .env e aggiungere il file .env al .gitignore

2. Latenza e Timeout delle Chiamate API:
- Problema: Le chiamate API possono essere molto lente e potrebbero causare timeout.
- Soluzione:
    - Implementare un timeout per le chiamate API e un meccanismo di retry per evitare che il programma si blocchi. 
    - Implementare un indicatore di caricamento (spinner) per mostrare all'utente che il programma sta lavorando.

3. Allucinazioni o Output AI non strutturato:
- Problema: Gemini potrebbe restituire output non strutturato o non coerente.
- Soluzione: Implementare un meccanismo di validazione per assicurare che l'output sia strutturato e coerente.

- Problema: Gemini potrebbe rispondere con una frase lunga invece di una singola parola (es. "Penso che il testo sia positivo") rendendo difficile il salvataggio su DB.
- Soluzione: Utilizzare Prompt Engineering specifico (es. "Rispondi solo con una parola: POSITIVO, NEGATIVO o NEUTRO") o forzare l'output in formato JSON.

4. Limiti di Token e Testi Lunghi:
- Problema: Se l'utente incolla un intero libro, potresti superare il limite di token del modello o i limiti della richiesta HTTP.
- Soluzione: 
    - Implementare un meccanismo di chunking per dividi il testo in blocchi più piccoli e processarli uno alla volta.
    - Implementare un controllo sulla lunghezza del testo in input e avvisare l'utente se il testo è troppo lungo prima di inviare la chiamata.

5. Concorrenza nel Database (SQLite):
- Problema: Se tenti di fare più analisi simultanee (caso raro in una CLI semplice, ma possibile), SQLite potrebbe restituire un errore di "Database locked".
- Soluzione: Gestire correttamente l'apertura e la chiusura delle connessioni al DB.

6. Gestione degli Errori:
- Problema: Se c'è un errore durante la chiamata all'API, potrebbe essere difficile capire quale errore è stato causato.
- Soluzione: Implementare un meccanismo di logging per registrare tutti gli errori e permettere all'utente di capire quale errore è stato causato.

7. Persistenza dei Dati:
- Problema: Se il programma si interrompe durante l'analisi, potrebbe essere difficile riprendere l'analisi.
- Soluzione: Implementare un meccanismo di persistenza dei dati per permettere all'utente di riprendere l'analisi.


**Requisiti Funzionali (Core)**
Il tool deve permettere all'utente di passare un testo (o un file) tramite riga di comando e ottenere:
- Word Count:  Calcolo locale di parole, caratteri e righe nel testo
- Sentiment Analysis: Integrazione con Gemini per determinare se il tono è Positivo, Negativo o Neutro, con un punteggio di confidenza.
- Persistence: Salvataggio automatico dei risultati in un database (TonyDB/JSON)

**Architettura del Sistema**
L'applciazione seguirà un flusso modulare:

1. Input: Lettura argomenti tramite CLI
2. Processing locale: Calcolo immediamo delle statistiche (Word Count)
3. AI Integration: Richiesta asincroma a Gemini per Sentiment Analysis
4. Database: Scrittura del record contenente:
    - ID
    - Testo
    - Word Count
    - Sentiment Analysis
    - Confidence
    - Timestamp
5. Output: Visualizzazione a terminale di un riepilogo formattato

**Stack Tecnologico**
- Linguaggio: Python
- AI SDK: Google Generative AI (Gemini)
- Database/Storage: JSON File / TinyDB (Scelta dettata dalla necessità di una struttura dati flessibile e di un formato facilmente leggibile anche esternamente al tool).
- CLI Parsing: argparse.
- Enviroment: Python-dotenv

**Suggerimenti per Feature Aggiuntive (Post-Core)**

- Analisi di File: Invece di passare una stringa, permettere il comando --file document.txt.
- Summarization: Chiedere a Gemini di generare un breve riassunto (max 20 parole).
- History Command: Un comando history per visualizzare le ultime 5 analisi salvate.
- Export: Opzione per esportare i report in Markdown o Google Sheets.
