from sqlalchemy import create_engine #connctDBtoFapi
from sqlalchemy.ext.declarative import declarative_base #DefORMmdls(tabls)
from sqlalchemy.orm import sessionmaker #intrctWithDB
from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#manageDB
Base = declarative_base()

def get_db(): #newDataSessionCreatedForEachAPIReq.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
