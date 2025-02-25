# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.models import ChatRequest, ChatResponse
from src.services.openai_service import OpenAIService
from src.services.vector_service import VectorService
from src.config import Settings
from src.utils import get_settings

app = FastAPI(
    title="AMC Information Chatbot API",
    description="API for Ahmedabad Municipal Corporation Information Chatbot",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services initialization
openai_service = None
vector_service = None

@app.on_event("startup")
async def startup_event():
    global openai_service, vector_service
    settings = get_settings()
    openai_service = OpenAIService(settings)
    vector_service = VectorService(settings)

@app.get("/")
async def root():
    return {"message": "Welcome to AMC Information Chatbot API"}

@app.get("/topics")
async def get_topics(settings: Settings = Depends(get_settings)):
    return {"topics": list(settings.NAMESPACE_MAP.keys())}

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    settings: Settings = Depends(get_settings)
):
    try:
        if request.topic not in settings.NAMESPACE_MAP:
            raise HTTPException(status_code=400, detail="Invalid topic")

        namespace = settings.NAMESPACE_MAP[request.topic]
        response = await openai_service.process_query(
            query=request.query,
            namespace=namespace,
            vector_service=vector_service
        )

        return ChatResponse(
            response=response,
            success=True,
            messages=[{"user": request.query, "bot": response}]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
