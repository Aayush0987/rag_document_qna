# services/conversation_service.py

from sqlalchemy.orm import Session
from db.models import Conversation


def list_conversations(db: Session, document_id: int = None):
    """List all conversations, optionally filtered by document_id."""
    query = db.query(Conversation)

    if document_id:
        query = query.filter(Conversation.document_id == document_id)

    return query.order_by(Conversation.timestamp.desc()).all()


def delete_conversation(db: Session, conversation_id: int):
    """Delete a single conversation by ID."""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conv:
        db.delete(conv)
        db.commit()
        return True
    return False


def delete_conversations_by_document(db: Session, document_id: int):
    """Delete all conversations for a document."""
    convs = db.query(Conversation).filter(Conversation.document_id == document_id).all()

    for c in convs:
        db.delete(c)

    db.commit()
    return len(convs)