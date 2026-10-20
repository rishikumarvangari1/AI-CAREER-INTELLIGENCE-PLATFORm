# career_engine.py

import re

from resume_parser import parse_resume
from skill_gap import analyze_skill_gap


SKILL_DICTIONARY = {
    "Python", "Java", "C", "C++", "C#", "JavaScript",
    "TypeScript", "HTML", "CSS", "React", "Angular",
    "Vue", "Node.js", "Express", "Flask", "Django",
    "Spring Boot", "SQL", "MySQL", "PostgreSQL",
    "MongoDB", "Git", "GitHub", "Maven", "Docker",
    "Kubernetes", "AWS", "Azure", "Linux", "REST API",
    "OOP", "Data Structures", "Algorithms", "Testing",
    "Excel", "Power BI", "Tableau", "Statistics",
    "Data Analysis", "Data Visualization", "Pandas",
    "NumPy", "Matplotlib", "Scikit-learn",
    "Machine Learning", "Deep Learning", "TensorFlow",
    "PyTorch", "NLP", "Generative AI", "LLM",
    "Communication", "Leadership", "Problem Solving",
    "Teamwork", "Project Management", "Cybersecurity",
    "Responsive Design", "Accessibility"
}


def extract_skills(text):
    """Detect known skill keywords without claiming proficiency."""
    found = []
    normalized = text.casefold()

    for skill in sorted(SKILL_DICTIONARY):
        pattern = (
            r"(?<![a-z0-9+#])"
            + re.escape(skill.casefold())
            + r"(?![a-z0-9+#])"
        )

        if re.search(pattern, normalized):
            found.append(skill)

    return sorted(set(found))


def detect_resume_sections(text, skills):
    """Estimate whether common resume sections are present."""
    return {
        "Contact information": bool(
            re.search(r"[\w.+-]+@[\w.-]+\.\w+", text)
        ),
        "Education": bool(
            re.search(
                r"\beducation\b|\buniversity\b|\bcollege\b|"
                r"\bdegree\b|\bbachelor\b|\bmaster\b",
                text,
                re.I
            )
        ),
        "Experience": bool(
            re.search(
                r"\bexperience\b|\bemployment\b|\binternship\b|"
                r"\bprofessional history\b",
                text,
                re.I
            )
        ),
        "Projects": bool(
            re.search(
                r"\bprojects?\b|\bportfolio\b",
                text,
                re.I
            )
        ),
        "Skills": bool(skills)
    }


def build_recommendations(text, sections, gap_result):
    recommendations = list(gap_result["recommendations"])

    if not sections["Projects"]:
        recommendations.append({
            "title": "Add practical projects",
            "description": (
                "Show relevant projects with technologies used, "
                "your contribution, and outcomes."
            )
        })

    if not sections["Education"]:
        recommendations.append({
            "title": "Review education details",
            "description": (
                "Include relevant qualifications and institution "
                "details where appropriate."
            )
        })

    if not sections["Contact information"]:
        recommendations.append({
            "title": "Review contact information",
            "description": (
                "Consider adding a professional email address and "
                "relevant portfolio or professional profile links."
            )
        })

    if len(text.split()) < 100:
        recommendations.append({
            "title": "Review resume content",
            "description": (
                "The extracted text is short. Verify that all pages "
                "and sections were read correctly."
            )
        })

    return recommendations[:10]


def analyze_career(text, role, filename="resume"):
    if not text or not text.strip():
        raise ValueError("The resume contains no readable text.")

    skills = extract_skills(text)
    sections = detect_resume_sections(text, skills)
    gap = analyze_skill_gap(skills, role)

    word_count = len(text.split())
    resume_score = round(
        sum(sections.values()) / len(sections) * 100
    )

    # Career readiness is a transparent heuristic, not a prediction.
    readiness = round(
        0.70 * gap["weighted_coverage"]
        + 0.30 * resume_score
    )

    years_found = re.findall(
        r"(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience",
        text,
        re.I
    )

    experience_years = max(
        (int(value) for value in years_found),
        default=0
    )

    recommendations = build_recommendations(
        text,
        sections,
        gap
    )

    # Fields here are deliberately compatible with script.js.
    return {
        "filename": filename,
        "role": role,
        "skills": skills,
        "skill_count": len(skills),
        "required_skills": gap["required_skills"],
        "matched_skills": gap["matched_skills"],
        "missing_skills": gap["missing_skills"],
        "match_score": gap["weighted_coverage"],
        "required_coverage": gap["required_coverage"],
        "readiness": readiness,
        "resume_score": resume_score,
        "word_count": word_count,
        "experience_years": experience_years,
        "sections": sections,
        "recommendations": recommendations,
        "skill_gap_count": gap["skill_gap_count"],
        "priority_skills": gap["priority_skills"]
    }


def analyze_resume_file(filepath, role, filename=None):
    """Convenience function for Flask routes."""
    text = parse_resume(filepath)

    return analyze_career(
        text=text,
        role=role,
        filename=filename or "resume"
    )