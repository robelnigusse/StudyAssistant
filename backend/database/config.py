from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base


load_dotenv()

db_url=os.getenv("DB_URL")
engine = create_engine(db_url)
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind = engine)
base = declarative_base()