from sqlalchemy.orm import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from .engine import Base
from datetime import datetime
import uuid


class JobScraped(Base):
    __tablename__ = "job_scraped"

    id = Column(Integer, primaryf_key=True, default= lambda: str(uuid.uuid4a()))
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    job_description = Column(String, nullable= False)
    location = Column(String, nullable=False)
    is_processed = Column(Boolean, default=False) # to track if agent has processed the JD
    time_stamped = Column(DateTime, default=datetime.utcnow)

class RunLog(Base):
    __tablename__ = "run_logs"

    id = Column(Integer, primary_key=True, default=lambda: str(uuid.uuid4()))
    version = Column(String, nullable=False) # This is a hash or fingerprint of the generated resume version.
    ats_score_before = Column(Float, nullable=False)
    ats_score_after = Column(Float, nullable=False)
    hallucinations = Column(Integer, nullable=False, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Foreign key relationship
    jd_id = Column(ForeignKey("job_scraped.id"), nullable=False)