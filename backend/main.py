import os
import sys

# Validate environment variables before booting the app
if not os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY") == "your_gemini_api_key_here":
    print("\n" + "="*70)
    print("❌ CRITICAL ERROR: GOOGLE_API_KEY is missing or invalid!")
    print("Please copy 'backend/.env.example' to 'backend/.env' and insert your actual Gemini API Key.")
    print("If you are using Docker, make sure the .env file exists before running docker compose up.")
    print("="*70 + "\n")
    sys.exit(1)

from fastapi import FastAPI
from database.config import engine, base
from database.models.conversations import Conversation
from database.models.messages import Message
from routes.conversation import router as conversation_router
from routes.message import router as message_router
from routes.book import router as book_router

from fastapi.middleware.cors import CORSMiddleware

base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversation_router)
app.include_router(message_router)
app.include_router(book_router)

@app.get("/")
async def root():
    return {"message": "working"}



