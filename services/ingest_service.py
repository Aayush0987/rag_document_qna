# services/ingest_service.py

import os
from sqlalchemy.orm import Session
from utils.file_reader import extract_text
from utils.chunker import chunk_text
from utils.embedding import embedder
from db.faiss_store import faiss_store
from db.models import Document, Chunk


UPLOAD_DIR = "uploaded_docs"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_file(file):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path


def ingest_document(file, db: Session):
    # 1. Save file locally
    file_path = save_file(file)

    # 2. Extract text
    text = extract_text(file_path)

    # 3. Chunk text
    chunks = chunk_text(text)

    # 4. Create document DB entry
    document = Document(
        filename=file.filename,
        file_type=file.filename.split(".")[-1]
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # 5. Insert chunks into DB
    for chunk in chunks:
        chunk_obj = Chunk(
            document_id=document.id,
            chunk_text=chunk
        )
        db.add(chunk_obj)
        db.commit()
        db.refresh(chunk_obj)

        # 6. Create embedding and store in FAISS
        embedding = embedder.get_embeddings([chunk])
        faiss_store.add_embeddings(embedding)

    return {
        "document_id": document.id,
        "total_chunks": len(chunks)
    }