from .MessageRepo import MessageRepo
from sentiments.SentimentRepo import SentimentRepo
from fastapi import Depends

class MessageService:
    def __init__(self, repo: MessageRepo = Depends(MessageRepo), sentiment: SentimentRepo = Depends(SentimentRepo)):
        self.repo = repo
        self.sentiment = sentiment

    async def create(self, message: dict):
        message["sentiment"] = await self.sentiment.getSentiment(message["content"])
        newMessage = self.repo.create(message)
        return newMessage
    
    def getAll(self)-> dict:
        return self.repo.getAll()
        