from fastapi import APIRouter
from ..services.personal_assistant_service import query
from pydantic import BaseModel


router = APIRouter()

class QueryModel(BaseModel):
    text: str



@router.post('/ask')
async def handled_query(payload: QueryModel):
    query_user = payload.text
    result = query(query_user)
    return {
        'status':'success',
        'response':result
    }