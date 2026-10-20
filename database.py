import os
import json
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "career_intelligence")
    )


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resume_analyses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                candidate_name VARCHAR(150),
                resume_filename VARCHAR(255) NOT NULL,
                target_role VARCHAR(150) NOT NULL,
                skills LONGTEXT,
                career_recommendations LONGTEXT,
                skill_gap LONGTEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def save_analysis(resume_filename, target_role, result):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        skills = result.get(
            "skills",
            result.get("extracted_skills", [])
        )

        recommendations = result.get(
            "career_recommendations",
            result.get("recommendations", result)
        )

        skill_gap = result.get(
            "skill_gap",
            result.get("skill_gap_analysis", {})
        )

        candidate_name = result.get("candidate_name")

        cursor.execute("""
            INSERT INTO resume_analyses (
                candidate_name,
                resume_filename,
                target_role,
                skills,
                career_recommendations,
                skill_gap
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            candidate_name,
            resume_filename,
            target_role,
            json.dumps(skills, ensure_ascii=False, default=str),
            json.dumps(recommendations, ensure_ascii=False, default=str),
            json.dumps(skill_gap, ensure_ascii=False, default=str)
        ))

        connection.commit()
        return cursor.lastrowid

    finally:
        cursor.close()
        connection.close()


def get_analysis_history(limit=50):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, candidate_name, resume_filename, target_role,
                   skills, career_recommendations, skill_gap, created_at
            FROM resume_analyses
            ORDER BY id DESC
            LIMIT %s
        """, (limit,))

        rows = cursor.fetchall()

        for row in rows:
            for key in ("skills", "career_recommendations", "skill_gap"):
                try:
                    row[key] = json.loads(row[key]) if row[key] else None
                except (json.JSONDecodeError, TypeError):
                    pass

            if row["created_at"]:
                row["created_at"] = row["created_at"].isoformat()

        return rows

    finally:
        cursor.close()
        connection.close()