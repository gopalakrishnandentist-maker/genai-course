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

## Week 2, Day 1: Reusable prompt for a 7-day South Indian meal plan

`w2-day1/meal_plan_prompt.md` is a prompt built on Role, Task, Context, Few-shot and Response. Change only the FOR block (age, weight, activity, allergies, dislikes, cooking time, household, city and month) and paste the rest into any AI chat tool.

The first draft left the calories to a guess, allowed dinners with no protein, put slow dishes on weekdays and let the model wrap the table in its own notes. The final version fixes each one, and two runs with different FOR blocks gave the same 28-row table with only the dishes and portions changing.

## Week 2, Day 2: JSON prompt template for Tamil scenes

`w2-day2/tamil_prompt.json` describes one scene field by field: a woman in a kandangi cotton sari drawing a pulli kolam in the courtyard of a Chettinad house in Karaikudi, Athangudi tiles and teak pillars, first light in Margazhi. Fields cover subject, setting (place, era, time of day), lighting, camera (shot, lens, angle), palette, style, aspect ratio and an avoid list. `w2-day2/prompts/` holds each run's JSON, with one field changed from the base.

On Gemini, changing `time_of_day` to golden hour came through muted because `lighting` still said cool skylight, and changing `shot` to close-up did nothing until `angle` stopped saying "pillars framing the courtyard". A one-field change only works when no other field describes the same thing. The video run added a `motion` block; Gemini returned 10 seconds at 16:9, so the posted clip is the first five seconds.

## Week 2, Day 3: Tracing a LangChain app with LangSmith

`w2-day3/traced_app.py` sends three prompts to gpt-4o-mini through LangChain's `ChatOpenAI`. The file has no tracing code: four environment variables switch LangSmith on and send the runs to a named project. `w2-day3/check_tracing.py` runs first and confirms tracing is on and the key is accepted, because tracing that is off fails silently.

The 250-word explainer prompt was the expensive one: 301 of 384 tokens, 86% of the cost and 3.94 s, driven by its 260 output tokens. The one-word classification took 36 tokens and 1.01 s. A call that failed on a 429 was traced too, with the prompt and the error.

## Week 2, Day 4: Multi-PDF RAG app with sources

`w2-day4/rag_app.py` is a Streamlit app that indexes several PDFs into one FAISS store and answers from the retrieved chunks with file and page for each. Tested on three sample clinic PDFs in `w2-day4/sample-pdfs/`, where the refund window is planted to disagree (7 against 14 working days): the app reported both sides with their pages instead of picking one. A Sunday-hours question first came back "Not found" although the right pages were retrieved; loosening the prompt's not-found rule fixed it without breaking the disagreement case.

## Week 2, Day 5: Five breakfast ideas from LangChain

`w2-day5/breakfast.py` asks gpt-4o-mini for five healthy South Indian breakfasts with the definition of healthy and the format pinned in the prompt, and prints only `reply.content`. Two runs gave different lists (millet pongal was the only repeat), the format held both times, and one run included rava dosa despite the whole-grain rule. Temperature 0 and protein grams on each line would make the output repeatable and checkable.
