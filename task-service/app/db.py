from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models import task, state
from app.settings import settings

engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
asyncSession = Database(settings.DATABASE_URI)

def init_db(db: Session) -> None:
    task.create(bind=engine)
    # state.create(bind=engine)
