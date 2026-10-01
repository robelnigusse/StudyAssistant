from fastapi import FastAPI

from database.config import engine, base
from database.models.conversations import Conversation
from database.models.messages import Message
from routes.conversation import router as conversation_router
from routes.message import router as message_router

base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(conversation_router)
app.include_router(message_router)

@app.get("/")
async def root():
    return {"message": "working"}



