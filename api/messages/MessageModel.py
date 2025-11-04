from pydantic import BaseModel, Field
import datetime
import uuid

class MessageModel(BaseModel):
    """Modello per il messaggio salvato nel 'database'."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    sentiment: str 
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class Message(BaseModel):
    """Modello per il messaggio in ricevuto dalla chiamata."""
    content: str