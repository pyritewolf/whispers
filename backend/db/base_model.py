from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, DateTime, ForeignKey, event
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.exc import IntegrityError

from db.session import SessionLocal


@as_declarative()
class BaseModel:
    "Base model for all entities"
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False
    )
