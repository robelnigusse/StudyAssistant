from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from services.rag_chain import ask_question
from database.config import get_db
from database.models.conversations import Conversation
from database.models.messages import Message
from schemas.message import MessageCreate, MessageResponse


router = APIRouter(
    prefix="/conversations",
    tags=["messages"]
)



from pydantic import BaseModel
class ChatResponse(BaseModel):
    answer: str
# CREATE MESSAGE
@router.post("/messages", response_model=ChatResponse)
def create_message(
    message: MessageCreate,
    conversation_id: UUID | None = None,
    db: Session = Depends(get_db)
):
    # If conversation_id was provided,
    # check that the conversation exists.
    if conversation_id is not None:
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

    # If no conversation_id was provided,
    # create a new conversation.
    else:
        conversation = Conversation(
            title=message.content[:50]
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        conversation_id = conversation.id

    # Create the message
    new_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=message.content
    )
    answer = ask_question(
        question=message.content,
    )
    ai_response = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=answer
    )
    
    db.add(new_message)
    db.add(ai_response)

    # Update conversation timestamp
    conversation.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(new_message)
    db.refresh(ai_response)
    return {
        "answer": answer,
    }


# GET ALL MESSAGES
@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
def get_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db)
):
    # Check if conversation exists
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

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    return messages

