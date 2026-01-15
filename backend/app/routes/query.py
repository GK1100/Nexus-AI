from fastapi import APIRouter
from pydantic import BaseModel
from app.services.query_service import query_service

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    session_id: str

@router.post("/")
def query_rag(req: QueryRequest):
    answer = query_service(req.question, req.session_id)
    return {"answer": answer}
