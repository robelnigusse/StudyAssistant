from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from database.config import get_db
from database.models.conversations import Conversation
from schemas.conversation import ConversationCreate, ConversationResponse


router = APIRouter(
    prefix="/conversations",
    tags=["conversations"]
)




# GET ALL
@router.get("/", response_model=list[ConversationResponse])
def get_conversations(
    db: Session = Depends(get_db)
):
    conversations = (
        db.query(Conversation)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    return conversations


# DELETE
@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db)
):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    db.delete(conversation)
    db.commit()

    return {
        "message": "Conversation deleted successfully"
    }