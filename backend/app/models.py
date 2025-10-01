from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    GESTOR = "gestor"
    VENDEDOR = "vendedor"
    INDICADOR = "indicador"

class LeadStatus(str, enum.Enum):
    NOVO = "novo"
    EM_CONTATO = "em_contato"
    EM_NEGOCIACAO = "em_negociacao"
    FECHADO = "fechado"
    PERDIDO = "perdido"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    city_state = Column(String(100), nullable=False)
    observation = Column(Text)
    status = Column(Enum(LeadStatus), default=LeadStatus.NOVO)
    
    indicador_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vendedor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    indicador = relationship("User", foreign_keys=[indicador_id])
    vendedor = relationship("User", foreign_keys=[vendedor_id])
