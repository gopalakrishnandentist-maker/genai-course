# GenAI course

Work from the Social Eagle Gen AI course, Batch 13.

## Week 1, Day 2: Student Grade Manager

`day2/grade_manager.py` is a menu program to add students and marks, show an aligned results table with grades, and report the class average, highest and lowest mark.

Run it with `python3 day2/grade_manager.py`.

Grades: 90 to 100 A, 80 to 89 B, 70 to 79 C, 60 to 69 D, below 60 E.

Invalid input (a mark outside 0 to 100, text instead of a number, an empty name, results requested before any student is added) prints a message and returns to the menu. Students are stored as a list, so two students with the same name are both kept.
