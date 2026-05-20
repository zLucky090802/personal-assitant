from fastapi import APIRouter
from ..services.personal_assistant_service import query, process_and_upload_file
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

class QueryModel(BaseModel):
    text: str


# Definimos la estructura de un mensaje individual
class ChatMessageModel(BaseModel):
    role: str     # 'user' o 'assistant'
    content: str


class ChatPayload(BaseModel):
    session_id: str  # Un ID único por usuario (ej: "user_12345")
    text: str        # La pregunta actual

@router.post('/ask')
async def handled_query(payload: QueryModel):
    query_user = payload.text
    result = query(query_user)
    return {
        'status':'success',
        'response':result
    }
    
@router.post('/upload')
async def upload_file(file:UploadFile = File(...)):
    """Endpoint genérico para subir e indexar cualquier archivo en tiempo real"""
    try:
        total_nodes = process_and_upload_file(file)
        return{
            "status": "success",
            "message": f"El archivo '{file.filename}' fue procesado e indexado con éxito.",
            "chunks_processed": total_nodes
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Fallo en la carga: {str(e)}')