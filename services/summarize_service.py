# services/summarize_service.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from db.models import Chunk
from sqlalchemy.orm import Session


# Load model once globally
model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def generate_summary(text):
    """Generate summary using LLM."""
    prompt = f"Summarize the following document:\n\n{text}\n\nSummary:"

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        inputs["input_ids"],
        max_length=250,
        num_beams=4,
        early_stopping=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def summarize_document(document_id: int, db: Session):
    """Collect all chunks from a document and create summary."""
    chunks = db.query(Chunk).filter(Chunk.document_id == document_id).all()

    if not chunks:
        return {"error": "Document not found or not yet processed."}

    # Combine all chunk texts
    full_text = "\n\n".join([c.chunk_text for c in chunks])

    # Generate summary
    summary = generate_summary(full_text)

    return {"document_id": document_id, "summary": summary}