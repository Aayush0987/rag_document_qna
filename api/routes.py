from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_route():
    return {"message": "Router working!"}

from services.summarize_service import summarize_document
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

from services.conversation_service import (
    list_conversations,
    delete_conversation,
    delete_conversations_by_document
)

@router.get("/conversations")
def get_conversations(document_id: int = None, db: Session = Depends(get_db)):
    conversations = list_conversations(db, document_id)
    return conversations

@router.delete("/conversations/{conversation_id}")
def delete_single(conversation_id: int, db: Session = Depends(get_db)):
    success = delete_conversation(db, conversation_id)
    if success:
        return {"message": "Conversation deleted."}
    return {"message": "Conversation not found."}

@router.delete("/conversations/document/{document_id}")
def delete_by_document(document_id: int, db: Session = Depends(get_db)):
    deleted_count = delete_conversations_by_document(db, document_id)
    return {"message": f"Deleted {deleted_count} conversations."}

@router.get("/summarize")
def summarize(document_id: int, db: Session = Depends(get_db)):
    return summarize_document(document_id, db)
