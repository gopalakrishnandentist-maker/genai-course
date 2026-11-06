# GenAI course

Work from the Social Eagle Gen AI course, Batch 13.

## Week 1, Day 2: Student Grade Manager

`day2/grade_manager.py` is a menu program to add students and marks, show an aligned results table with grades, and report the class average, highest and lowest mark.

Run it with `python3 day2/grade_manager.py`.

Grades: 90 to 100 A, 80 to 89 B, 70 to 79 C, 60 to 69 D, below 60 E.

Invalid input (a mark outside 0 to 100, text instead of a number, an empty name, results requested before any student is added) prints a message and returns to the menu. Students are stored as a list, so two students with the same name are both kept.

## Week 1, Day 3: Live cricket score with Playwright

`day3/cricbuzz_score.py` opens Cricbuzz with Playwright's sync API, waits for the first match card to appear (no fixed sleep), prints the card text and saves `score.png`.

Setup: `python3 -m venv venv`, `source venv/bin/activate`, `pip install playwright`, `playwright install chromium`.

Run it with `python cricbuzz_score.py`. It runs headed by default. Cricbuzz returns Access Denied to a headless browser, so `--headless` makes the script print that and exit with code 1 instead of crashing. The same happens if no match card appears within 20 seconds.

## Week 1, Day 4: Student Grade Manager in Streamlit

`day4/grade_app.py` is the Day 2 grade manager as a Streamlit page: a form to add a student and mark, a table with grades, and the class average, highest and lowest as metrics. Same grading scale as Day 2 (90 to 100 A, 80 to 89 B, 70 to 79 C, 60 to 69 D, below 60 E). An empty name is rejected, and the mark box only accepts 0 to 100.

Setup: `python3 -m venv venv`, `source venv/bin/activate`, `pip install streamlit`.

Run it with `streamlit run grade_app.py`.

The student list lives in `st.session_state`. Streamlit reruns the whole file on every click, so a plain `students = []` at the top is reset each time and adding a second student wipes the first.
