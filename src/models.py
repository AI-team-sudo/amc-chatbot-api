# src/models.py
from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    user: str
    bot: str

class ChatRequest(BaseModel):
    query: str
    topic: str

class ChatResponse(BaseModel):
    response: str
    success: bool
    messages: Optional[List[Message]]
