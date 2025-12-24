from fastapi import FastAPI
from db.database import Base, engine
from api.routes import router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routes (empty for now)
app.include_router(router)

@app.get("/")
def home():
    return {"status": "RAG System Setup Successful"}