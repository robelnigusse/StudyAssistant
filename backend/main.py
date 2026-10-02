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



