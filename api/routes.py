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