
import os
from urllib.parse import quote_plus
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Azure MySQL Configuration
user = quote_plus(os.environ["DB_USER"])
password = quote_plus(os.environ["DB_PASSWORD"])
host = os.environ["DB_HOST"]
database = os.environ["DB_NAME"]

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{user}:{password}@{host}:3306/{database}"
    "?ssl_ca=/etc/ssl/certs/ca-certificates.crt"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Student Database Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course = db.Column(db.String(100), nullable=False)


# Home Page - Frontend UI
@app.route("/")
def home():
    return render_template("index.html")


# Get All Students
@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()

    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "course": s.course
        }
        for s in students
    ])


# Add New Student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    if not data or not all(data.get(k) for k in ["name", "email", "course"]):
        return jsonify({
            "error": "Name, email and course are required"
        }), 400

    student = Student(
        name=data["name"],
        email=data["email"],
        course=data["course"]
    )

    try:
        db.session.add(student)
        db.session.commit()

        return jsonify({
            "message": "Student added successfully",
            "id": student.id
        }), 201

    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Unable to add student. Check whether the email already exists."
        }), 400


# Delete Student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    })


# Create Database Table
with app.app_context():
    db.create_all()


# Run Application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
