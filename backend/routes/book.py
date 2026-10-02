from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from uuid import UUID

from services.load_pdf import upload_and_process_pdf
from database.config import get_db
from database.models.conversations import Conversation
from schemas.conversation import ConversationCreate, ConversationResponse


router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/upload")
def upload_book(file: UploadFile = File(...)):
    upload_and_process_pdf(file)

    return {"message": "Book uploaded successfully"}

