from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from engine import SentinelEngine

app = FastAPI(title="Sentinel IQ API")

# Libera acesso para o Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = SentinelEngine()

class QuestionRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": "Sentinel IQ Online"}

@app.post("/ask")
async def ask(request: QuestionRequest):
    try:
        response = engine.ask_question(request.text)
        #return {"answer": response["result"]}
        return {"answer": response["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest():
    try:
        engine.ingest_documents()
        return {"message": "Documentos indexados com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)