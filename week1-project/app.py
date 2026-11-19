"""Student Grade Manager, Week 1 project.

Run it with:
    streamlit run app.py

Grade logic lives in grades.py. This file is only the page.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from grades import (
    GRADE_ORDER,
    PASS_MARK,
    Student,
    from_csv,
    get_grade,
    grade_counts,
    summary,
    to_csv,
    validate,
)

SAMPLE = Path(__file__).parent / "sample_students.csv"

st.set_page_config(page_title="Student Grade Manager", page_icon="📘", layout="wide")

if "students" not in st.session_state:
    st.session_state.students = []
students = st.session_state.students


# ---------- Sidebar: add, import, export ----------
with st.sidebar:
    st.header("Add a student")
    with st.form("add", clear_on_submit=True):
        name = st.text_input("Name", placeholder="e.g. Priya")
        mark = st.number_input("Mark (0 to 100)", min_value=0, max_value=100, step=1, value=0)
        if st.form_submit_button("Add student", type="primary", width="stretch"):
            problem = validate(name, mark)
            if problem:
                st.error(problem)
            else:
                students.append(Student(name.strip(), int(mark)))
                st.toast(f"Added {name.strip()} ({int(mark)}, grade {get_grade(int(mark))})")

    if st.button("Load sample class", width="stretch", disabled=not SAMPLE.exists()):
        loaded, _ = from_csv(SAMPLE.read_text())
        students.extend(loaded)
        st.toast(f"Loaded {len(loaded)} sample students")
    with st.expander("Import from CSV"):
        upload = st.file_uploader("CSV with Name and Mark columns", type="csv")
        if upload is not None and st.button("Import", width="stretch"):
            loaded, errors = from_csv(upload.getvalue().decode("utf-8-sig"))
            students.extend(loaded)
            if loaded:
                st.success(f"Imported {len(loaded)} students.")
            for err in errors:
                st.warning(err)

    st.divider()
    st.download_button(
        "Download results (CSV)",
        data=to_csv(students),
        file_name="grades.csv",
        mime="text/csv",
        disabled=not students,
        width="stretch",
    )
    if st.button("Clear all", disabled=not students, width="stretch"):
        students.clear()
        st.rerun()

    st.caption("Grades: 90+ A, 80+ B, 70+ C, 60+ D, below 60 E. Pass mark 60.")


# ---------- Main page ----------
st.title("Student Grade Manager")
st.caption("Add students in the sidebar or import a CSV. Edit marks or delete rows in the table.")

stats = summary(students)
if stats is None:
    st.info("No students yet. Add one in the sidebar, or import a CSV.")
    st.stop()

cols = st.columns(5)
cols[0].metric("Students", stats["count"])
cols[1].metric("Average", stats["average"])
cols[2].metric("Highest", stats["highest"])
cols[3].metric("Lowest", stats["lowest"])
cols[4].metric("Pass rate", f"{stats['pass_rate']}%")

left, right = st.columns([3, 2])

with left:
    st.subheader("Results")
    query = st.text_input("Search by name", placeholder="Type to filter", label_visibility="collapsed")
    table = pd.DataFrame(
        {
            "Name": [s.name for s in students],
            "Mark": [s.mark for s in students],
            "Grade": [get_grade(s.mark) for s in students],
            "Delete": [False] * len(students),
        }
    )
    shown = table[table["Name"].str.contains(query, case=False, regex=False)] if query else table
    edited = st.data_editor(
        shown,
        key=f"editor-{query}-{len(students)}",
        hide_index=True,
        width="stretch",
        disabled=["Grade"],
        column_config={
            "Mark": st.column_config.NumberColumn(min_value=0, max_value=100, step=1),
            "Delete": st.column_config.CheckboxColumn(help="Tick to remove this student"),
        },
    )
    # The editor keeps the original row positions as its index, so edits map back to the list.
    changed = False
    for pos, row in edited.iterrows():
        if (row["Name"] or "").strip() and validate(row["Name"], row["Mark"]) is None:
            new = Student(row["Name"].strip(), int(row["Mark"]))
            if new != students[pos]:
                students[pos] = new
                changed = True
    to_delete = sorted(edited.index[edited["Delete"]].tolist(), reverse=True)
    for pos in to_delete:
        del students[pos]
    if changed or to_delete:
        st.rerun()

with right:
    st.subheader("Grades")
    counts = grade_counts(students)
    chart = pd.DataFrame({"Grade": GRADE_ORDER, "Students": [counts[g] for g in GRADE_ORDER]})
    st.bar_chart(chart, x="Grade", y="Students", height=260, color="#1F6F5C")

    below = [s for s in students if s.mark < PASS_MARK]
    if below:
        names = ", ".join(f"{s.name} ({s.mark})" for s in below)
        st.warning(f"**Needs support** (below {PASS_MARK}): {names}")
