# Job Description Parser
from ats_lab.db.crud import get_job_description
from ats_lab.db.engine import SessionLocal

def parse_job_description(db, jd_id):
    """ Parses a job description by its ID """
    jd_entry = get_job_description(db, jd_id)
    if jd_entry:
        jd_text = jd_entry.job_description
        # Add parsing logic here
        parsed_data = {
            "title": jd_entry.title,
            "company": jd_entry.company,
            "location": jd_entry.location,
            "description": jd_text,
            # More parsed fields can be added here
        }
        return parsed_data
    else:
        print(f"No job description found with ID {jd_id}")
        return None
    
if __name__ == "__main__":
    db = SessionLocal()
    jd_id = 1  # Example job description ID
    parsed_jd = parse_job_description(db, jd_id)
    if parsed_jd:
        print("Parsed Job Description:", parsed_jd)