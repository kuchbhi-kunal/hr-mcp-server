from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any

# ----------------------------------------------------------------------
# Teacher & Student Data
# ----------------------------------------------------------------------

teacher_data: Dict[str, Dict[str, Any]] = {
    "Anita": {
        "subject": "Mathematics",
        "students": ["Kunal", "Rohit", "Sara"],
        "schedule": {
            "Monday": "10:00 AM - 11:00 AM",
            "Wednesday": "2:00 PM - 3:00 PM",
            "Friday": "9:00 AM - 10:00 AM"
        },
        "attendance": {
            "Kunal": 92,
            "Rohit": 87,
            "Sara": 95
        },
        "grades": {
            "Kunal": "A",
            "Rohit": "B+",
            "Sara": "A+"
        }
    },
    "Brian": {
        "subject": "Science",
        "students": ["Kunal", "Liam", "Maya"],
        "schedule": {
            "Tuesday": "11:00 AM - 12:00 PM",
            "Thursday": "3:00 PM - 4:00 PM"
        },
        "attendance": {
            "Kunal": 89,
            "Liam": 91,
            "Maya": 85
        },
        "grades": {
            "Kunal": "A-",
            "Liam": "A",
            "Maya": "B"
        }
    }
}

mcp = FastMCP("SheltonTeacher")

@mcp.tool()
def get_teacher_subject(teacher_name: str) -> str:
    """Return the subject taught by a given teacher."""
    data = teacher_data.get(teacher_name)
    if data:
        return f"{teacher_name} teaches {data['subject']}."
    return "Teacher not found."

@mcp.tool()
def get_teacher_schedule(teacher_name: str) -> str:
    """Get the teaching schedule of a specific teacher."""
    data = teacher_data.get(teacher_name)
    if not data:
        return "Teacher not found."

    schedule = "\n".join([f"{day}: {time}" for day, time in data["schedule"].items()])
    return f"Schedule for {teacher_name}:\n{schedule}"

@mcp.tool()
def list_students(teacher_name: str) -> str:
    """List all students under a teacher."""
    data = teacher_data.get(teacher_name)
    if not data:
        return "Teacher not found."
    students = ", ".join(data["students"])
    return f"Students under {teacher_name}: {students}"

@mcp.tool()
def get_student_grade(teacher_name: str, student_name: str) -> str:
    """Get a student's grade from a specific teacher."""
    data = teacher_data.get(teacher_name)
    if not data:
        return "Teacher not found."
    grade = data["grades"].get(student_name)
    if grade:
        return f"{student_name} has a grade of {grade} in {data['subject']}."
    return f"{student_name} is not found in {teacher_name}'s class."

@mcp.tool()
def update_student_grade(teacher_name: str, student_name: str, new_grade: str) -> str:
    """Update a student's grade."""
    data = teacher_data.get(teacher_name)
    if not data:
        return "Teacher not found."
    if student_name not in data["students"]:
        return f"{student_name} is not in {teacher_name}'s class."
    data["grades"][student_name] = new_grade
    return f"Updated {student_name}'s grade to {new_grade} in {data['subject']}."

@mcp.tool()
def get_student_attendance(teacher_name: str, student_name: str) -> str:
    """Check the attendance percentage of a student."""
    data = teacher_data.get(teacher_name)
    if not data:
        return "Teacher not found."
    attendance = data["attendance"].get(student_name)
    if attendance is not None:
        return f"{student_name}'s attendance in {data['subject']} is {attendance}%."
    return f"{student_name} not found in {teacher_name}'s class."

@mcp.tool()
def mark_attendance(teacher_name: str, student_name: str, present: bool) -> str:
    """Mark attendance (increase percentage slightly if present)."""
    data = teacher_data.get(teacher_name)
    if not data:
        return "Teacher not found."
    if student_name not in data["students"]:
        return f"{student_name} is not in {teacher_name}'s class."

    current = data["attendance"].get(student_name, 0)
    if present:
        new_value = min(100, current + 1)
        data["attendance"][student_name] = new_value
        return f"Marked present. {student_name}'s attendance is now {new_value}%."
    else:
        new_value = max(0, current - 1)
        data["attendance"][student_name] = new_value
        return f"Marked absent. {student_name}'s attendance is now {new_value}%."


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Personalized greeting for a teacher or student."""
    return f"Hello {name}! How can I assist you with your class or students today?"

@mcp.tool()
def wish_happy_teachers_day() -> str:
    """Wish teachers a Happy Teacher's Day."""
    art = """
    🎓  Happy Teacher's Day! 🎓
    ----------------------------
    To all the mentors who guide, inspire,
    and make learning a joy — thank you!
    🌸📘✨
    """
    return art

@mcp.tool()
def what_is_your_name() -> str:
    """Return the assistant's name"""
    return "My name is SheltonTeacher."

@mcp.tool()
def are_you_a_teacher() -> str:
    """Respond to role inquiry"""
    return "No, I’m not a teacher — I’m the Faculty Assistant."


if __name__ == "__main__":
    mcp.run()
