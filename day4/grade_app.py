"""Student Grade Manager as a Streamlit page, Week 1 Day 4.

Run it with:
    streamlit run grade_app.py

Why session_state: Streamlit reruns this whole file every time someone clicks
anything. A plain `students = []` at the top is reset to empty on every rerun,
so adding a second student wipes the first. st.session_state is the one place
that survives the rerun, so the list lives there.

Same logic as Day 2: grades A to E on the same scale, and a list of
(name, mark) tuples so two students can share a name.
"""

import streamlit as st


def get_grade(mark):
    """Return the grade letter for a mark from 0 to 100 (same scale as Day 2)."""
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "E"


st.title("Student Grade Manager")

if "students" not in st.session_state:
    st.session_state.students = []

with st.form("add", clear_on_submit=True):
    name = st.text_input("Name")
    mark = st.number_input("Mark (0 to 100)", min_value=0, max_value=100, step=1)
    submitted = st.form_submit_button("Add")

if submitted:
    name = name.strip()
    if not name:
        st.error("The name cannot be empty. Nothing was added.")
    elif not 0 <= mark <= 100:
        st.error("The mark must be from 0 to 100. Nothing was added.")
    else:
        st.session_state.students.append((name, mark))

students = st.session_state.students

if students:
    st.dataframe(
        [{"Name": n, "Mark": m, "Grade": get_grade(m)} for n, m in students],
        hide_index=True,
        width="stretch",
    )
    marks = [m for _, m in students]
    average, highest, lowest = st.columns(3)
    average.metric("Average", f"{sum(marks) / len(marks):.1f}")
    highest.metric("Highest", max(marks))
    lowest.metric("Lowest", min(marks))
else:
    st.info("No students yet. Add one above.")
