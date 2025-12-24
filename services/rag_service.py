# services/rag_service.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from utils.embedding import embedder
from db.faiss_store import faiss_store
from db.models import Chunk, Conversation
from sqlalchemy.orm import Session
import numpy as np


# Load model once
model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def generate_answer(context, question):
    """Generate final answer using context + question."""
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        inputs["input_ids"],
        max_length=300,
        num_beams=4,
        early_stopping=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def rag_query(document_id: int, question: str, db: Session, top_k=3):

    # Step 1: Generate embedding for question
    query_embedding = embedder.get_embedding(question)

    # Step 2: Search FAISS for top-k similar chunks
    distances, indices = faiss_store.search(query_embedding, k=top_k)

    # Step 3: Retrieve chunk text from DB
    chunk_texts = []
    for i in indices[0]:
        if i == -1:
            continue
        chunk_obj = db.query(Chunk).filter(Chunk.id == i + 1).first()
        if chunk_obj:
            chunk_texts.append(chunk_obj.chunk_text)

    # Combine context
    context = "\n\n".join(chunk_texts)

    # Step 4: Generate answer
    answer = generate_answer(context, question)

    # Step 5: Save conversation
    conv = Conversation(
        document_id=document_id,
        question=question,
        answer=answer
    )
    db.add(conv)
    db.commit()

    return {
        "answer": answer,
        "source_chunks": chunk_texts
    }