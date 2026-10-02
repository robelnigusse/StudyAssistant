from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from uuid import UUID

from services.load_pdf import upload_and_process_pdf, get_all_books, delete_book
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

@router.get("/")
def list_books():
    books = get_all_books()
    return {"books": books}

@router.delete("/{filename}")
def remove_book(filename: str):
    success = delete_book(filename)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
