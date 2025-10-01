from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import models, schemas
from sqlalchemy.orm import Session
import bcrypt

SQLALCHEMY_DATABASE_URL = "sqlite:///./indicavende.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_lead(db: Session, lead: schemas.LeadCreate, indicador_id: int):
    db_lead = models.Lead(
        **lead.dict(),
        indicador_id=indicador_id
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_all_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lead).offset(skip).limit(limit).all()

def get_indicador_leads(db: Session, indicador_id: int):
    return db.query(models.Lead).filter(models.Lead.indicador_id == indicador_id).all()

def get_vendedor_leads(db: Session, vendedor_id: int):
    return db.query(models.Lead).filter(models.Lead.vendedor_id == vendedor_id).all()

def update_lead_status(db: Session, lead_id: int, lead_update: schemas.LeadUpdate):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not db_lead:
        return None
    
    for field, value in lead_update.dict(exclude_unset=True).items():
        setattr(db_lead, field, value)
    
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
