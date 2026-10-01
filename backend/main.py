from database.config import engine, base
from database.models.conversation import Conversation
from database.models.message import Message


base.metadata.create_all(bind=engine)
print("Database tables created successfully.")