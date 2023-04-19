import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column, 
    DateTime, 
    String, 
    Enum as SqlaEnum, 
    Integer,
) 


class Base(DeclarativeBase):
    pass


class ScientometricDatabase(str, Enum):
    scopus = "Scopus"
    wos = "WOS"
    risc = "RISC"

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creation_date = Column(DateTime, default=datetime.utcnow)
    full_name = Column(String)
    scientometric_database = Column(SqlaEnum(ScientometricDatabase))
    publication_count = Column(Integer)
    citation_count = Column(Integer)
    h_index = Column(Integer)
    url = Column(String)
