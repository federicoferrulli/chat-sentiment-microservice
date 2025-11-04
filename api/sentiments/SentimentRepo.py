from .SentimentModel import SentimentModel
import random
from fastapi import Depends
import asyncio
from dotenv import load_dotenv 
from os import environ
from pathlib import Path

current_file_path = Path(__file__)
root_dir = current_file_path.parent.parent
env_path = root_dir / ".env" 
load_dotenv(dotenv_path=env_path)


class SentimentRepo:
    def __init__(self):
        self.model = SentimentModel

    async def getSentiment(self, text: str) -> SentimentModel:        
        delay = random.uniform(float(environ.get("DELAYMIN", 0.1)), float(environ.get("DELAYMAX", 0.5)))
        
        await asyncio.sleep(delay)
        
        
        if random.random() < 0.1:
            raise IOError("Simulated sentiment service is down")

        sentiment = random.choice(list(self.model))
        return sentiment

