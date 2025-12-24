from fastapi import FastAPI
from db.database import Base, engine
from api.routes import router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include router
app.include_router(router)

@app.get("/")
def home():
    return {"status": "RAG System Setup Successful"}