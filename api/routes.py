from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_route():
    return {"message": "Router working!"}


from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.ingest_service import ingest_document

router = APIRouter()

@router.post("/upload")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    result = ingest_document(file, db)
    return {
        "message": "Document uploaded successfully",
        "document_id": result["document_id"],
        "chunks_created": result["total_chunks"]
    }

from services.rag_service import rag_query

@router.post("/ask")
def ask_question(document_id: int, question: str, db: Session = Depends(get_db)):
    result = rag_query(document_id, question, db)
    return result