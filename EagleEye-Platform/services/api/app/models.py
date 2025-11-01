from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from .db import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String)  # owner/gc/sub/lender/partner
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    contacts = relationship("Contact", back_populates="account", cascade="all, delete")

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"))
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    role = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    account = relationship("Account", back_populates="contacts")

class Project(Base):
    __tablename__ = "projects"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"))
    name = Column(String, nullable=False)
    jurisdiction = Column(String)
    address = Column(Text)
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class File(Base):
    __tablename__ = "files"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    name = Column(String)
    mime = Column(String)
    path = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Finding(Base):
    __tablename__ = "findings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    severity = Column(String)  # red/orange/yellow/info
    discipline = Column(String)
    location = Column(String)
    code_citation = Column(String)
    impact = Column(Text)
    recommendation = Column(Text)
    ve_alt = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Estimate(Base):
    __tablename__ = "estimates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    payload = Column(Text)  # JSON string (base/alternates/allowances/summary)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
