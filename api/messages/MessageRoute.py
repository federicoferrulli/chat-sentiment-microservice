from fastapi import FastAPI, Request, Depends
from .MessageModel import Message, MessageModel
from .MessageService import MessageService

router = FastAPI()

@router.get(
        "/messages",
        tags=["Messages"],
        summary="Restituisce un array di tutti i messaggi salvati in memoria",
        status_code=200,
        description="Restituisce un array di tutti i messaggi salvati in memoria",
        response_description="Lista di messaggi",
        response_model = dict
    )
async def getAll(req: Request, service: MessageService = Depends(MessageService)):
    messages: list = service.getAll()
    return {
        "request_id": req.state.request_id,
        "results": messages
    }

@router.post(
        "/messages",
        tags=["Messages"],
        summary="Inserisci un nuovo messaggio in memoria",
        status_code=200,
        description="Salva un messaggio inserendo un 'Sentiment' al messaggio",
        response_description="Restituisce il messaggio inserito in memoria",
        response_model = dict
    )
async def create(req: Request, service: MessageService = Depends(MessageService)):
    newMessage: Message = await req.json()
    results: MessageModel = await service.create(newMessage)
    return {
        "request_id": req.state.request_id,
        "results": results
    }
    