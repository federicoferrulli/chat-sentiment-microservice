# Chat-Sentiment Microservice

Servizio per analizzare e salvare il sentiment di messaggi.

Questo progetto è un microservizio basato su FastAPI che espone API per inviare messaggi, analizzarne (in modo simulato) il sentiment e salvarli in memoria.

## Prerequisiti

  * Python 3.10+
  * `pip` (Python package installer)

## 1\. Installazione (Build)

1.  **Clonare il repository** (se applicabile)

    ```bash
    git clone https://github.com/federicoferrulli/chat-sentiment-microservice.git
    cd chat-sentiment-microservice
    ```

2.  **Creare un ambiente virtuale** (consigliato)

    ```bash
    python -m venv venv
    source venv/bin/activate  # Su Windows: venv\Scripts\activate
    ```
4.  **Installare le dipendenze**
    Una volta attivato l'ambiente virtuale, esegui:

    ```bash
    pip install -r requirements.txt
    ```

## 2\. Configurazione

Il servizio utilizza un file `.env` per configurare il comportamento della simulazione del sentiment.

1.  **Creare il file .env**
    Nella directory `api/`, creare un file chiamato `.env`.

2.  **Aggiungere le variabili d'ambiente**
    Incollare il seguente contenuto nel file `api/.env`:

    ```ini
    # Ritardo massimo (secondi) per la simulazione dell'analisi
    DELAYMAX = 0.5

    # Ritardo minimo (secondi)
    DELAYMIN = 0.1

    # Ambiente di sviluppo. "DEV" mostra gli stack trace negli errori
    ENVIROMENT = "DEV"
    ```

## 3\. Esecuzione (Run)

Per avviare il server API, utilizzare `fastapi`. Il file di ingresso è `api/index.py` e l'oggetto app FastAPI si chiama `app`.

```bash

fastapi run .\api\index.py
```

Il server sarà ora in ascolto su `http://localhost:8000`.

## 4\. Test (Utilizzo API)

È possibile testare gli endpoint utilizzando `curl` o qualsiasi client API (come Postman).

### Endpoint di Health Check

Controlla lo stato del servizio.

```bash
curl http://localhost:8000/api/health
```

**Risposta (Esempio):**

```json
{
  "request_id": "a1b2c3d4-...",
  "code": 200,
  "msg": "pong!",
  "path": "/api/health",
  "status": "ok",
  "timestamp": "2025-11-05T09:30:00.123456"
}
```

### Inserire un nuovo messaggio

Invia un nuovo messaggio per l'analisi e il salvataggio.

```bash
curl -X POST http://localhost:8000/api/messages \
     -H "Content-Type: application/json" \
     -d '{"content": "Questo è un ottimo servizio!"}'
```

**Risposta (Esempio):**

```json
{
  "request_id": "e5f6g7h8-...",
  "results": {
    "id": "f9a8b7c6-...",
    "content": "Questo è un ottimo servizio!",
    "sentiment": "positive",
    "created_at": "2025-11-05T09:31:00.567890"
  }
}
```

### Ottenere tutti i messaggi

Recupera tutti i messaggi salvati in memoria.

```bash
curl http://localhost:8000/api/messages
```

**Risposta (Esempio):**

```json
{
  "request_id": "x1y2z3a4-...",
  "results": {
    "f9a8b7c6-...": {
      "id": "f9a8b7c6-...",
      "content": "Questo è un ottimo servizio!",
      "sentiment": "positive",
      "created_at": "2025-11-05T09:31:00.567890"
    }
  }
}
```