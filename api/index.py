import importlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import routes
from middleware.LoggerMiddleware import LoggerMiddleware
from middleware.ErrorMiddleware import ErrorMiddleware


app = FastAPI(   
    title="Chat-Sentiment Microservice",
    description="Servizio per analizzare e salvare il sentiment di messaggi.",
    version="1.0.0"
)

origins: list[str] = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggerMiddleware)
app.add_middleware(ErrorMiddleware)

for route in routes.routes:
    try:
        modulePath = route["from"]   
        routerName = route["import"] 
        prefix = route["prefix"]
        module = importlib.import_module(modulePath)        
        router = getattr(module, routerName)
        app.include_router(router.router, prefix=prefix)        

        print(f"INFO: Rotta caricata: {prefix} da {modulePath}.{routerName}")
    except (ImportError, AttributeError) as e:
        print(f"ERRORE: Impossibile caricare la rotta {route}: {e}")


