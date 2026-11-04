"""Student Grade Manager, Week 1 Day 2.

Storage choice: a list of (name, mark) tuples. A list keeps the order the
students were added and allows two students with the same name, because two
people can both be called Priya. A dictionary keyed by name would silently
overwrite the first one.
"""

students = []


def get_grade(mark):
    """Return the grade letter for a mark from 0 to 100."""
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "E"


def read_mark(text):
    """Turn typed text into a mark between 0 and 100, or return None."""
    try:
        mark = float(text.strip())
    except ValueError:
        return None
    if mark != mark or mark < 0 or mark > 100:  # mark != mark catches nan
        return None
    return int(mark) if mark == int(mark) else mark


def add_student():
    """Ask for a name and a mark, check both, then store them."""
    name = input("Student name: ").strip()
    if not name:
        print("The name cannot be empty. Nothing was added.")
        return
    mark = read_mark(input("Mark (0 to 100): "))
    if mark is None:
        print("The mark must be a number from 0 to 100. Nothing was added.")
        return
    students.append((name, mark))
    print(f"Added {name} with {mark} ({get_grade(mark)}).")


def show_results():
    """Print an aligned table, then the average, highest and lowest mark."""
    if not students:
        print("No students yet. Add one first.")
        return
    width = max(len("Name"), max(len(name) for name, _ in students))
    print(f"{'Name':<{width}}  {'Mark':>6}  {'Grade':>5}")
    for name, mark in students:
        print(f"{name:<{width}}  {mark:>6}  {get_grade(mark):>5}")
    marks = [mark for _, mark in students]
    average = sum(marks) / len(marks)
    print(f"Average: {average:.1f}    Highest: {max(marks)}    Lowest: {min(marks)}")


def main():
    while True:
        print("\n1. Add a student\n2. Show results\n3. Quit")
        try:
            choice = input("Choose 1, 2 or 3: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return
        if choice == "1":
            try:
                add_student()
            except (EOFError, KeyboardInterrupt):
                print("\nInput stopped. Nothing was added.")
                return
        elif choice == "2":
            show_results()
        elif choice == "3":
            print("Goodbye.")
            return
        else:
            print("Please type 1, 2 or 3.")


if __name__ == "__main__":
    main()
