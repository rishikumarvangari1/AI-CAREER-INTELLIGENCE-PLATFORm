# skill_gap.py

ROLE_REQUIREMENTS = {
    "Python Developer": {
        "required": [
            "Python", "OOP", "SQL", "Git",
            "REST API", "Testing"
        ],
        "important": [
            "Flask", "Django", "Data Structures", "Algorithms"
        ],
        "bonus": ["Docker", "AWS", "PostgreSQL"]
    },

    "Data Analyst": {
        "required": [
            "SQL", "Excel", "Statistics", "Data Analysis"
        ],
        "important": [
            "Python", "Pandas", "Power BI",
            "Tableau", "Data Visualization"
        ],
        "bonus": ["AWS", "Machine Learning", "PostgreSQL"]
    },

    "AI/ML Engineer": {
        "required": [
            "Python", "Machine Learning", "Statistics",
            "Data Analysis"
        ],
        "important": [
            "Deep Learning", "NumPy", "Pandas",
            "Scikit-learn", "SQL"
        ],
        "bonus": [
            "TensorFlow", "PyTorch", "NLP",
            "Generative AI", "LLM"
        ]
    },

    "Frontend Developer": {
        "required": [
            "HTML", "CSS", "JavaScript", "Responsive Design"
        ],
        "important": [
            "React", "Git", "REST API", "Testing"
        ],
        "bonus": ["TypeScript", "Node.js", "Accessibility"]
    },

    "Java Developer": {
        "required": [
            "Java", "OOP", "SQL", "REST API"
        ],
        "important": [
            "Spring Boot", "Git", "Maven", "Testing"
        ],
        "bonus": ["Docker", "AWS", "PostgreSQL"]
    }
}


def analyze_skill_gap(resume_skills, role):
    """
    Compare resume keywords with a role-specific skill profile.

    Scores are rule-based coverage indicators, not measurements
    of real-world proficiency or hiring probability.
    """
    if role not in ROLE_REQUIREMENTS:
        raise ValueError(f"Unsupported career role: {role}")

    skill_lookup = {
        skill.casefold(): skill
        for skill in resume_skills
    }

    requirements = ROLE_REQUIREMENTS[role]

    matched = []
    missing = []
    priorities = []

    weights = {
        "required": 3,
        "important": 2,
        "bonus": 1
    }

    weighted_total = 0
    weighted_matched = 0

    for category in ("required", "important", "bonus"):
        for skill in requirements[category]:
            weight = weights[category]
            weighted_total += weight

            if skill.casefold() in skill_lookup:
                matched.append(skill)
                weighted_matched += weight
            else:
                missing.append(skill)

                priorities.append({
                    "skill": skill,
                    "priority": category,
                    "weight": weight,
                    "reason": (
                        "Core requirement for the selected role."
                        if category == "required"
                        else
                        "Useful skill for the selected role."
                        if category == "important"
                        else
                        "Additional skill that may strengthen your profile."
                    )
                })

    required = requirements["required"]

    required_matched = sum(
        1 for skill in required
        if skill.casefold() in skill_lookup
    )

    required_coverage = round(
        required_matched / len(required) * 100
    ) if required else 0

    weighted_coverage = round(
        weighted_matched / weighted_total * 100
    ) if weighted_total else 0

    priority_order = {
        "required": 0,
        "important": 1,
        "bonus": 2
    }

    priorities.sort(
        key=lambda item: (
            priority_order[item["priority"]],
            item["skill"]
        )
    )

    return {
        "role": role,
        "required_skills": (
            requirements["required"]
            + requirements["important"]
            + requirements["bonus"]
        ),
        "matched_skills": matched,
        "missing_skills": missing,
        "required_coverage": required_coverage,
        "weighted_coverage": weighted_coverage,
        "skill_gap_count": len(missing),
        "priority_skills": priorities,
        "recommendations": [
            {
                "title": f"Develop {item['skill']}",
                "description": (
                    f"{item['reason']} Study the fundamentals, "
                    "practice with exercises, and demonstrate the "
                    "skill through a practical project."
                )
            }
            for item in priorities[:5]
        ]
    }