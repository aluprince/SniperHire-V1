from .models import RunLog, JobScraped
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


# get all job descriptions that are not processed in the db

def get_unprocessed_job_descriptions(db: Session):
    """ Get all job descriptions that are not processed in the db"""
    try:
        job_description = db.query(JobScraped).filter(JobScraped.is_processed == False).all()
        return job_description
    except SQLAlchemyError as e:
        print(f"Error retrieving unprocessed job descriptions")
        print("Error details:", str(e))

def get_processed_job_descriptions(db: Session):
    """ Get all job descriptions that are processed in the db"""
    try:
        job_description_processed = db.query(JobScraped).filter(JobScraped.is_processed == True).all()
        return job_description_processed
    except SQLAlchemyError as e:
        print(f"Error retrieving processed job descriptions")
        print("Error details:", str(e))

def get_job_description(db: Session, jd_id: int):
    """ Get a job description by its ID"""
    try:
        job_description = db.query(JobScraped).filter(JobScraped.id == jd_id).first()
        return job_description
    except SQLAlchemyError as e:
        print(f"Error retrieving job description with ID {jd_id}")
        print("Error details:", str(e))