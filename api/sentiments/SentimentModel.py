from enum import Enum
class SentimentModel(Enum):   
    """Enumerazione per i possibili sentiment."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"