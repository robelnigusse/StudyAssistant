from database.config import engine, base
from backend.database.models.conversations import Conversation
from backend.database.models.messages import Message


base.metadata.create_all(bind=engine)
