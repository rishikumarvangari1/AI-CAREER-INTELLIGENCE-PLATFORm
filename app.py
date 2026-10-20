from dotenv import load_dotenv

load_dotenv()

import os
import uuid
from pathlib import Path

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from resume_parser import (
    parse_resume,
    ResumeParsingError,
    SUPPORTED_EXTENSIONS
)
from career_engine import analyze_career
from database import (
    initialize_database,
    save_analysis,
    get_analysis_history
)


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


ROLES = [
    "Python Developer",
    "Data Analyst",
    "AI/ML Engineer",
    "Frontend Developer",
    "Java Developer"
]


def save_uploaded_file(uploaded):
    if not uploaded or not uploaded.filename:
        raise ValueError("Please select a file.")

    original_name = secure_filename(uploaded.filename)

    if not original_name or "." not in original_name:
        raise ValueError("Invalid filename.")

    extension = Path(original_name).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(
            f"Unsupported file type. Supported formats: {supported}"
        )

    filename = f"{uuid.uuid4().hex}{extension}"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    uploaded.save(filepath)

    return filepath, original_name


def validate_role(role):
    if role not in ROLES:
        raise ValueError("Please select a valid career role.")


def analyze_uploaded_resume(uploaded, role):
    filepath = None

    try:
        validate_role(role)

        filepath, original_name = save_uploaded_file(uploaded)

        text = parse_resume(filepath)

        result = analyze_career(
            text=text,
            role=role,
            filename=original_name
        )

        if not isinstance(result, dict):
            raise RuntimeError(
                "The career engine returned an unexpected result."
            )

        initialize_database()

        analysis_id = save_analysis(
            resume_filename=original_name,
            target_role=role,
            result=result
        )

        result["analysis_id"] = analysis_id
        result["saved_to_database"] = True

        return result

    finally:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)


@app.route("/")
def index():
    return render_template("index.html", roles=ROLES)


@app.route("/api/analyze", methods=["POST"])
def analyze_api():
    try:
        role = request.form.get("role", "Python Developer")

        result = analyze_uploaded_resume(
            request.files.get("resume"),
            role
        )

        return jsonify(result)

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    except ResumeParsingError as exc:
        return jsonify({"error": str(exc)}), 422

    except Exception:
        app.logger.exception("Career analysis failed")

        return jsonify({
            "error": (
                "Analysis or database saving failed. "
                "Check your MySQL connection and application terminal."
            )
        }), 500


@app.route("/api/history", methods=["GET"])
def analysis_history():
    try:
        initialize_database()

        history = get_analysis_history(limit=50)

        return jsonify({
            "count": len(history),
            "analyses": history
        })

    except Exception:
        app.logger.exception("Unable to retrieve analysis history")

        return jsonify({
            "error": "Unable to retrieve analysis history."
        }), 500


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "GET":
        return render_template("index.html", roles=ROLES)

    try:
        role = request.form.get("role", "Python Developer")

        result = analyze_uploaded_resume(
            request.files.get("resume"),
            role
        )

        return render_template(
            "result.html",
            result=result
        )

    except ValueError as exc:
        return str(exc), 400

    except ResumeParsingError as exc:
        return str(exc), 422

    except Exception:
        app.logger.exception("Report generation failed")

        return (
            "Unable to generate or save the report. "
            "Please check the application terminal.",
            500
        )


@app.errorhandler(413)
def file_too_large(error):
    message = "The uploaded file exceeds the 10 MB limit."

    if request.path in ("/api/analyze", "/api/history"):
        return jsonify({"error": message}), 413

    return message, 413


if __name__ == "__main__":
    app.run(debug=True)