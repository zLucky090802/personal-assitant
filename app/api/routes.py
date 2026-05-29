from fastapi import APIRouter
from ..services.personal_assistant_service import chat_with_history, process_and_upload_file
from pydantic import BaseModel
from ..schemas.assistant_schema import ChatPayload
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post('/ask')
async def handled_query(payload: ChatPayload):
    
    try:
        session_id = payload.session_id
        query_user = payload.text
        
        result = await chat_with_history(session_id=session_id, query_text=query_user)
        
        return result
    
    except Exception as e:
        print(f'Error en el enpoint /ask: {e}')
        raise HTTPException(status_code=500, detail=f'Error interno en el chat: {str(e)}')
    
@router.post('/upload')
async def upload_file(file: UploadFile = File(...)): # <-- 1. Aquí se recibe de Postman
    try:
        # 2. OJO AQUÍ: Debes pasarle el objeto 'file' completo al servicio
        total_nodes = process_and_upload_file(file) 
        
        if total_nodes == 0:
            return {
                "status": "success",
                "message": f"El archivo '{file.filename}' ya se encuentra disponible y optimizado.",
                "chunks_processed": 0
            }
            
        return {
            "status": "success",
            "message": f"El archivo '{file.filename}' fue procesado e indexado con éxito.",
            "chunks_processed": total_nodes
        }
    except Exception as e:
        print(f'Error en el servicio al procesar archivo: {e}')
        # Si algo falla en el servicio, este string captura el error y lo muestra en Postman
        raise HTTPException(status_code=500, detail=f"Fallo en la carga: {str(e)}")