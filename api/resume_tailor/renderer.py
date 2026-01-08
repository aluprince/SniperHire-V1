from weasyprint import HTML
from jinja2 import Template
import os

def generate_tailored_resume(tailored_json, master_resume, output_filename="Tailored_Resume.pdf"):
    # THE TEMPLATE (ATS-Optimized with WeasyPrint support)
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            @page { size: A4; margin: 0.5in; }
            body { font-family: 'Arial', sans-serif; font-size: 10pt; line-height: 1.4; color: #000; margin: 0; padding: 0; }
            .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 5px; margin-bottom: 12px; }
            .name { font-size: 18pt; font-weight: bold; text-transform: uppercase; }
            .contact { font-size: 9pt; margin-top: 4px; }
            .section-title { font-size: 11pt; font-weight: bold; text-transform: uppercase; border-bottom: 1px solid #000; margin-top: 15px; margin-bottom: 8px; background-color: #f2f2f2; padding: 2px 5px; }
            .item-header { display: flex; justify-content: space-between; font-weight: bold; }
            .item-sub { font-style: italic; font-size: 9.5pt; }
            ul { margin-top: 3px; margin-bottom: 8px; padding-left: 20px; }
            li { margin-bottom: 2px; }
            .skills-line { margin-bottom: 4px; }
            .bold { font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="name">{{ name }}</div>
            <div class="contact">📧 {{ email }} | 📍 {{ location }} | 🔗 {{ github }}</div>
        </div>

        <div class="section-title">Professional Summary</div>
        <p>{{ summary }}</p>

        <div class="section-title">Technical Skills</div>
        <div class="skills-line"><span class="bold">Languages:</span> {{ languages }}</div>
        <div class="skills-line"><span class="bold">Frameworks:</span> {{ frameworks }}</div>
        <div class="skills-line"><span class="bold">Tools & DevOps:</span> {{ tools }}</div>
        <div class="skills-line"><span class="bold">Core Concepts:</span> {{ concepts }}</div>

        <div class="section-title">Professional Experience</div>
        {% for job in experience %}
        <div class="item-header">
            <span>{{ job.role }}</span>
            <span>{{ job.dates }}</span>
        </div>
        <div class="item-sub">{{ job.company }}</div>
        <ul>{% for bullet in job.bullets %}<li>{{ bullet }}</li>{% endfor %}</ul>
        {% endfor %}

        <div class="section-title">Key Projects</div>
        {% for proj in projects %}
        <div class="item-header"><span>{{ proj.name }}</span></div>
        <ul>{% for bullet in proj.bullets %}<li>{{ bullet }}</li>{% endfor %}</ul>
        {% endfor %}

        <div class="section-title">Education</div>
        {% for edu in education %}
        <div class="item-header">
            <span>{{ edu.degree }}</span>
            <span>{{ edu.status }}</span>
        </div>
        <div class="item-sub">{{ edu.institution }}</div>
        <div style="font-size: 9pt; color: #444;">{{ edu.highlights }}</div>
        {% endfor %}
    </body>
    </html>
    """

    # --- RUTHLESS LOGIC MERGE ---
    master_skills = master_resume.get("master_skills", {})
    cat_skills = tailored_json.get("categorized_skills", {})

    def merge_cat(key, master_list):
        # Combines master data with LLM-tailored keywords, ensures unique title-case entries
        tailored_list = cat_skills.get(key, [])
        return ", ".join(sorted(set([s.title() for s in (master_list + tailored_list)])))

    data = {
        "name": master_resume['contact']['name'],
        "email": master_resume['contact']['email'],
        "location": master_resume['contact']['location'],
        "github": master_resume['contact']['github'],
        "summary": tailored_json.get("professional_summary", ""),
        "languages": merge_cat("languages", master_skills.get("languages", [])),
        "frameworks": merge_cat("frameworks", master_skills.get("frameworks", [])),
        "tools": merge_cat("tools_devops", master_skills.get("tools_devops", [])),
        "concepts": merge_cat("concepts", master_skills.get("concepts", [])),
        "experience": tailored_json.get("experience", []),
        "projects": tailored_json.get("projects", []),
        "education": master_resume.get("education", [])
    }

    # Render Template
    template = Template(html_template)
    final_html = template.render(data)

    # Convert to PDF using WeasyPrint (Ruthless Integrity)
    HTML(string=final_html).write_pdf(output_filename)
    
    return output_filename