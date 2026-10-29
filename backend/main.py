
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.chatbot import generate_response, conversations

app = FastAPI(
    title="StudyMate AI",
    description="Context-aware Gemini chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    conversation_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=10000)


class ChatResponse(BaseModel):
    conversation_id: str
    response: str


@app.get("/")
def home():
    return {"message": "StudyMate AI backend is running!"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer = await generate_response(
            request.conversation_id,
            request.message
        )

        return ChatResponse(
            conversation_id=request.conversation_id,
            response=answer
        )

    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))


@app.post("/api/new-chat")
def new_chat():
    conversation_id = str(uuid4())
    conversations[conversation_id] = []

    return {
        "conversation_id": conversation_id,
        "message": "New conversation created."
    }
