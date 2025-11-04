# Chat-Sentiment Microservice

## 1\. Introduzione

Questo documento descrive l'architettura e il design del **Chat-Sentiment Microservice**. Lo scopo del servizio è analizzare e salvare il sentiment (positivo, negativo, neutrale) dei messaggi inviati tramite API, utilizzando un'architettura basata su FastAPI.

## 2\. Architettura

Il servizio adotta un'architettura a layer (livelli) costruita sul framework FastAPI, sfruttando la Dependency Injection (DI) per separare le responsabilità.

  * **Livello Route (API):** Gestito da `FastAPI`. I moduli `MessageRoute.py` e `HealthRoute.py` definiscono gli endpoint HTTP. Le rotte vengono caricate dinamicamente all'avvio come specificato in `config/routes.py` dall'entripoint `index.py`.
  * **Livello Service (Logica Applicativa):** Rappresentato da `MessageService.py`. Questo livello orchestra la logica di business: riceve i dati dalle rotte, coordina l'analisi del sentiment (chiamando `SentimentRepo`) e il salvataggio dei dati (chiamando `MessageRepo`).
  * **Livello Repository (Accesso Dati):**
      * `MessageRepo.py`: Gestisce l'accesso ai dati. Attualmente è un'implementazione *in-memory* che salva i messaggi in un dizionario Python.
      * `SentimentRepo.py`: Simula un servizio esterno di analisi del sentiment. Introduce un ritardo configurabile (tramite `.env`) e può simulare errori (10% di probabilità di `IOError`) per testare la resilienza.

## 3\. Componenti Chiave

### Entripoint (`index.py`)

Il file `index.py` è il punto di ingresso dell'applicazione.

1.  Inizializza l'istanza principale `FastAPI`.
2.  Configura il `CORSMiddleware` per consentire richieste da origini specifiche (es. `http://localhost:3000`).
3.  Registra i middleware custom:
      * `LoggerMiddleware`
      * `ErrorMiddleware`
4.  Legge la configurazione da `config/routes.py` e carica dinamicamente i router (es. `HealthRoute`, `MessageRoute`) usando `importlib`.

### Middleware

I middleware intercettano ogni richiesta prima che raggiunga le rotte e prima che la risposta venga inviata.

  * **`LoggerMiddleware` (`middleware/LoggerMiddleware.py`):**
      * Genera un `request_id` univoco (UUID) per ogni richiesta.
      * Salva il `request_id` nello stato della richiesta (`request.state.request_id`) affinché sia accessibile in altri punti dell'app (es. log, risposte).
      * Stampa un log di accesso iniziale con timestamp, metodo, path e IP.
  * **`ErrorMiddleware` (`middleware/ErrorMiddleware.py`):**
      * Avvolge la chiamata alla rotta (`call_next`) in un blocco `try...except Exception`.
      * Se si verifica un'eccezione (sia `HTTPException` che eccezioni Python generiche), la cattura.
      * Logga l'errore e restituisce una `JSONResponse` standard contenente `request_id`, `status_code`, `message` e lo `stack` trace (solo se `ENVIROMENT` è "DEV").

### Modelli Dati (`messages/MessageModel.py`)

Vengono usati modelli Pydantic per la validazione e la serializzazione:

  * `Message`: Modello per l'input della richiesta POST (solo `content: str`).
  * `MessageModel`: Modello per i dati salvati "nel database" (in-memory); include `id` (UUID), `content`, `sentiment` e `created_at` (datetime).

## 4\. Flusso Dati (POST /api/messages)

1.  Una richiesta `POST /api/messages` con JSON `{"content": "..."}` arriva al server.
2.  `LoggerMiddleware` genera un `request_id` (es. "abc-123") e lo logga.
3.  `MessageRoute` (`@router.post("/messages")`) riceve la richiesta.
4.  FastAPI (tramite DI) crea un'istanza di `MessageService`, che a sua volta riceve istanze di `MessageRepo` e `SentimentRepo`.
5.  La rotta chiama `await service.create(newMessage)`.
6.  `MessageService` chiama `await self.sentiment.getSentiment(...)`.
7.  `SentimentRepo` attende per un tempo casuale (es. 0.3s) e restituisce un `SentimentModel` (es. `POSITIVE`).
8.  *(Scenario Errore):* Se `SentimentRepo` solleva un `IOError`, `ErrorMiddleware` la cattura e restituisce un JSON 500.
9.  *(Scenario Successo):* `MessageService` aggiunge il sentiment al messaggio.
10. `MessageService` chiama `self.repo.create(message)`.
11. `MessageRepo` crea un `MessageModel` (con nuovo ID e timestamp) e lo salva nel dizionario `elements`.
12. Il `MessageModel` completo viene restituito come risposta JSON dalla rotta.