from xhtml2pdf import pisa
from jinja2 import Template
import os

def generate_tailored_resume(tailored_json, master_resume, output_filename="Tailored_Resume.pdf"):
    # 1. The Claude HTML Template with Jinja2 Placeholders
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            @page { size: a4; margin: 0.5in; }
            body { font-family: 'Helvetica', 'Arial', sans-serif; font-size: 11pt; line-height: 1.4; color: #000; }
            .header { text-align: center; border-bottom: 1px solid #000; padding-bottom: 10px; margin-bottom: 15px; }
            .section { margin-bottom: 15px; }
            .section-title { font-size: 12pt; font-weight: bold; text-transform: uppercase; border-bottom: 1px solid #000; margin-bottom: 8px; }
            .job-header { font-weight: bold; }
            ul { margin-left: 20px; }
            li { font-size: 10.5pt; margin-bottom: 3px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{{ name }}</h1>
            <div>📧 {{ email }} | 📍 {{ location }} | 🔗 {{ linkedin }}</div>
        </div>

        <div class="section">
            <div class="section-title">Professional Summary</div>
            <p>{{ summary }}</p>
        </div>

        <div class="section">
            <div class="section-title">Professional Experience</div>
            {% for job in experience %}
            <div style="margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <span class="job-header">{{ job.role }}</span>
                    <span>{{ job.dates }}</span>
                </div>
                <div style="font-style: italic;">{{ job.company }}</div>
                <ul>
                    {% for bullet in job.bullets %}
                    <li>{{ bullet }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
        </div>

        <div class="section">
            <div class="section-title">Key Projects</div>
            {% for proj in projects %}
            <div style="margin-bottom: 8px;">
                <div class="job-header">{{ proj.name }}</div>
                <ul>
                    {% for bullet in proj.bullets %}
                    <li>{{ bullet }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
        </div>

        <div class="section">
            <div class="section-title">Technical Skills</div>
            <div>
                <strong>Skills:</strong> {{ skills }}
            </div>
        </div>
    </body>
    </html>
    """

    # 2. Prepare Data for Injection
    contact = master_resume.get("contact", {})
    # Merge master skills with tailored unmatched skills for a full profile
    combined_skills = ", ".join(set(master_resume.get("skills", []) + tailored_json.get("unmatched_skills", [])))

    data = {
        "name": contact.get("name", "Candidate"),
        "email": contact.get("email", ""),
        "location": contact.get("location", "Remote"),
        "linkedin": contact.get("linkedin", ""),
        "summary": tailored_json.get("professional_summary", ""),
        "experience": tailored_json.get("experience", []),
        "projects": tailored_json.get("projects", []),
        "skills": combined_skills
    }

    # 3. Render HTML with Jinja2
    template = Template(html_template)
    final_html = template.render(data)

    # 4. Convert to PDF
    with open(output_filename, "wb") as f:
        pisa_status = pisa.CreatePDF(final_html, dest=f)
    
    return not pisa_status.err