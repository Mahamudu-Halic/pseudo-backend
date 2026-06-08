from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import Session
from datetime import datetime
from database import Base

class Region(Base):
    __tablename__ = "regions"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class MMDA(Base):
    __tablename__ = "mmdas"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    region_id = Column(String, index=True)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    display_name = Column(String)
    phone = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="citizen")  # citizen, minister, glinax
    region = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class ProblemCategory(Base):
    __tablename__ = "problem_categories"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    region = Column(String)
    mmda = Column(String)
    community = Column(String, nullable=True)
    category = Column(String)
    title = Column(String)
    description = Column(Text)
    severity = Column(String)  # low, medium, high
    ghana_postgps = Column(String, nullable=True)
    file_url = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, in_progress, resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
