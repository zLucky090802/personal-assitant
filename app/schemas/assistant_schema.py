from pydantic import BaseModel

class QueryModel(BaseModel):
    text: str

# Definimos la estructura de un mensaje individual
class ChatMessageModel(BaseModel):
    role: str     # 'user' o 'assistant'
    content: str

class ChatPayload(BaseModel):
    session_id: str  # Un ID único por usuario (ej: "user_12345")
    text: str        # La pregunta actual