"""Grade logic for the Student Grade Manager. No Streamlit here, so it can be tested on its own."""

import csv
import io
from dataclasses import dataclass

# (lowest mark for the grade, grade letter), highest first. Same scale as Week 1 Day 2.
GRADE_SCALE = [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (0, "E")]
GRADE_ORDER = [letter for _, letter in GRADE_SCALE]
PASS_MARK = 60


@dataclass
class Student:
    name: str
    mark: int


def get_grade(mark):
    """Return the grade letter for a mark from 0 to 100."""
    if not 0 <= mark <= 100:
        raise ValueError(f"Mark must be from 0 to 100, got {mark}")
    for lowest, letter in GRADE_SCALE:
        if mark >= lowest:
            return letter
    return "E"


def validate(name, mark):
    """Return an error message, or None if the name and mark are acceptable."""
    if not name or not name.strip():
        return "The name cannot be empty."
    if not isinstance(mark, (int, float)) or not 0 <= mark <= 100:
        return "The mark must be a number from 0 to 100."
    return None


def summary(students):
    """Class statistics. Returns None when there are no students."""
    if not students:
        return None
    marks = [s.mark for s in students]
    passed = sum(1 for m in marks if m >= PASS_MARK)
    return {
        "count": len(marks),
        "average": round(sum(marks) / len(marks), 1),
        "highest": max(marks),
        "lowest": min(marks),
        "pass_rate": round(100 * passed / len(marks)),
    }


def grade_counts(students):
    """Number of students per grade, every grade present (zero if none)."""
    counts = {letter: 0 for letter in GRADE_ORDER}
    for s in students:
        counts[get_grade(s.mark)] += 1
    return counts


def to_csv(students):
    """Students as CSV text with Name, Mark and Grade columns."""
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["Name", "Mark", "Grade"])
    for s in students:
        writer.writerow([s.name, s.mark, get_grade(s.mark)])
    return out.getvalue()


def from_csv(text):
    """Read students from CSV text with Name and Mark columns.

    Returns (students, errors). Rows that fail validation are skipped and
    reported by line number, so one bad row does not block the whole file.
    """
    reader = csv.DictReader(io.StringIO(text))
    fields = {(f or "").strip().lower(): f for f in (reader.fieldnames or [])}
    if "name" not in fields or "mark" not in fields:
        return [], ["The file needs a header row with Name and Mark columns."]
    students, errors = [], []
    for line, row in enumerate(reader, start=2):
        name = (row.get(fields["name"]) or "").strip()
        raw = (row.get(fields["mark"]) or "").strip()
        try:
            mark = int(float(raw))
        except ValueError:
            errors.append(f"Line {line}: mark '{raw}' is not a number.")
            continue
        problem = validate(name, mark)
        if problem:
            errors.append(f"Line {line}: {problem}")
            continue
        students.append(Student(name, mark))
    return students, errors
