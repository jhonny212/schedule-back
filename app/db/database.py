from sqlalchemy import create_engine, text 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)
db = SessionLocal()
Base = declarative_base()
session = Session(bind=engine)


def excute_query(query):
    with engine.connect() as conn:
        return conn.execute(text(query))
        
def get_entity_by_id(entity,id,custom_ref=None):
    if custom_ref:
        return db.query(entity).filter(custom_ref == id).first()
    return db.query(entity).filter(entity.Id == id).first()