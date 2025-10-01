from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from . import models, schemas, auth, database
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IndicaVende API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/login", response_model=schemas.UserResponse)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return user

@app.post("/auth/register", response_model=schemas.UserResponse)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth.create_user(db, user_data)

@app.post("/leads/", response_model=schemas.LeadResponse)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    return database.create_lead(db, lead, current_user.id)

@app.get("/leads/", response_model=List[schemas.LeadResponse])
def get_leads(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    if current_user.role == "gestor":
        return database.get_all_leads(db, skip, limit)
    elif current_user.role == "vendedor":
        return database.get_vendedor_leads(db, current_user.id)
    else:
        return database.get_indicador_leads(db, current_user.id)

@app.put("/leads/{lead_id}", response_model=schemas.LeadResponse)
def update_lead_status(
    lead_id: int, 
    lead_update: schemas.LeadUpdate, 
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    if current_user.role not in ["vendedor", "gestor"]:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar leads")
    return database.update_lead_status(db, lead_id, lead_update)

@app.get("/users/", response_model=List[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    if current_user.role != "gestor":
        raise HTTPException(status_code=403, detail="Acesso negado")
    return database.get_all_users(db)

@app.get("/vendedores/", response_model=List[schemas.UserResponse])
def get_vendedores(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_user)
):
    return database.get_vendedores(db)

@app.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    return auth.seed_database(db)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
