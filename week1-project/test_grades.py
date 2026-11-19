import pytest

from grades import Student, from_csv, get_grade, grade_counts, summary, to_csv, validate


@pytest.mark.parametrize(
    "mark, grade",
    [(100, "A"), (90, "A"), (89, "B"), (80, "B"), (79, "C"), (70, "C"), (69, "D"), (60, "D"), (59, "E"), (0, "E")],
)
def test_grade_boundaries(mark, grade):
    assert get_grade(mark) == grade


@pytest.mark.parametrize("mark", [-1, 101])
def test_grade_rejects_out_of_range(mark):
    with pytest.raises(ValueError):
        get_grade(mark)


def test_validate():
    assert validate("Priya", 92) is None
    assert validate("  ", 50) is not None
    assert validate("Arun", 120) is not None


def test_summary_and_counts():
    students = [Student("Priya", 92), Student("Arun", 78), Student("Divya", 55)]
    stats = summary(students)
    assert stats == {"count": 3, "average": 75.0, "highest": 92, "lowest": 55, "pass_rate": 67}
    assert grade_counts(students) == {"A": 1, "B": 0, "C": 1, "D": 0, "E": 1}
    assert summary([]) is None


def test_csv_round_trip():
    students = [Student("Priya", 92), Student("Priya", 61)]
    loaded, errors = from_csv(to_csv(students))
    assert loaded == students and errors == []


def test_csv_skips_bad_rows():
    loaded, errors = from_csv("Name,Mark\nPriya,92\n,70\nArun,abc\nDivya,140\n")
    assert loaded == [Student("Priya", 92)]
    assert len(errors) == 3 and errors[0].startswith("Line 3")


def test_csv_needs_header():
    loaded, errors = from_csv("Priya,92\n")
    assert loaded == [] and errors
