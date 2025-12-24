from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "RAG System Setup Successful"}