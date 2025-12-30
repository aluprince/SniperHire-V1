# models.py
from sqlalchemy import Column, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from .engine import Base
from datetime import datetime
import uuid


class JobScraped(Base):
    __tablename__ = "job_scraped"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False
    )
    job_title = Column(String, nullable=False)
    company_name = Column(String, default="N/A")
    job_description = Column(Text)  # Text for long descriptions
    job_url = Column(String, unique=True, index=True, nullable=False)
    location = Column(String)
    source = Column(String, nullable=False)
    applied = Column(Boolean, default=False)
    match_score = Column(Float, nullable=True)
    is_processed = Column(Boolean, default=False)
    time_stamped = Column(DateTime(timezone=True), default=datetime.utcnow)


class JobApplication(Base):
    __tablename__ = "job_application"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False
    )

    resume_tailored = Column(Text, nullable=False)
    cover_letter_tailored = Column(Text, nullable=True)
    applied_at = Column(String, nullable=True) # e.g, Source platform
    approval_status = Column(String, default="Pending") # e.g, Pending, Approved, Rejected
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    jd_id = Column(UUID(as_uuid=True), ForeignKey("job_scraped.id"), nullable=False, index=True)

class RunLog(Base):
    __tablename__ = "run_logs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )
    version = Column(String, nullable=False)
    ats_score_before = Column(Float, nullable=False)
    ats_score_after = Column(Float, nullable=False)
    hallucinations = Column(Float, default=0)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)

    jd_id = Column(UUID(as_uuid=True), ForeignKey("job_scraped.id"), nullable=False, index=True)