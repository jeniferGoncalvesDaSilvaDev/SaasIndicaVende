from sqlalchemy.orm import Session
from . import models, schemas, database
import bcrypt
from fastapi import Depends, HTTPException, Header
from typing import Optional
import os

SECRET_KEY = os.getenv("SESSION_SECRET", "indicavende-secret-key-change-in-production")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(db: Session, email: str, password: str):
    user = database.get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return False
    return user

def create_user(db: Session, user: schemas.UserCreate):
    db_user = database.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    hashed_password = hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_current_user(db: Session = Depends(database.SessionLocal), user_email: Optional[str] = Header(None, alias="X-User-Email")):
    if not user_email:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    user = database.get_user_by_email(db, email=user_email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def seed_database(db: Session):
    users_data = [
        {"name": "Admin", "email": "admin@indicavende.me", "password": "admin123", "role": "gestor"},
        {"name": "Juliano", "email": "juliano@indicavende.me", "password": "seller123", "role": "vendedor"},
        {"name": "Pedro", "email": "pedro@indicavende.me", "password": "indicator123", "role": "indicador"},
        {"name": "Daniela", "email": "daniela@indicavende.me", "password": "seller123", "role": "vendedor"},
    ]
    
    for user_data in users_data:
        if not database.get_user_by_email(db, user_data["email"]):
            create_user(db, schemas.UserCreate(**user_data))
    
    db.commit()
    return {"message": "Database seeded successfully"}
