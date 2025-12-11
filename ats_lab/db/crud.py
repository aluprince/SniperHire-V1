from .models import RunLog
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def log_run(db, jd_id, version, ats_score_before, ats_score_after, hallucinations):
    """ insert a new log row for calculating ats score """
    try:
        entry = RunLog(jd_id=jd_id,
                        version=version,
                        ats_score_before=ats_score_before,
                        ats_score_after=ats_score_after,
                        hallucinations=hallucinations)
        
        db.add(entry)
        db.commit()
        db.refresh(entry)
    except SQLAlchemyError as e:
        print("Error logging run:", e)
        db.rollback()
        return None

def get_all_logs(db):
    """returns all RunLogs entry"""
    return db.query(RunLog).all()

def get_runs_by_jd(db, jd_id):
    filtered_jd = db.query(RunLog).where(RunLog.jd_id == jd_id).all()
    return filtered_jd