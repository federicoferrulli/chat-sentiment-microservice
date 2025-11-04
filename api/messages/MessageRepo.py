from .MessageModel import MessageModel
elements: dict =  {}

class MessageRepo:
    def __init__(self):
        self.model = MessageModel

    def create(self, message: dict) -> MessageModel:
        newMessage: MessageModel = self.model(**message)
        elements[newMessage.id] = newMessage
        return newMessage
    
    def getAll(self)-> dict:
        return elements