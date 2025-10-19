import os
import subprocess
from datetime import datetime

if os.path.exists("goal.txt"):
    with open("goal.txt", "r") as f:
        lines = f.readlines()
        if len(lines) > 1:
            deadline_str = lines[1].strip()
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
            if deadline > datetime.now():
                print("Wait until the first goal is complete...")
                subprocess.run(["python", "checker.py"])
                quit()

goal = NotImplemented
while goal == NotImplemented or not goal:
    goal = input("Enter your goal: ")

days = {"SUN": 6, "MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5}
deadline = None
while deadline not in days:
    deadline = input("Enter deadline day [SUN, MON, TUE, WED, THU, FRI, SAT]: ").upper()

    if deadline == "DEB":
        break

    if deadline not in days:
        print("Invalid day. Try again.")

if deadline != "DEB":
    current_date = datetime.today()

    timedelta = days[deadline] - current_date.weekday()
    if timedelta <= 0:
        timedelta += 7

    due_date = datetime(
        current_date.year, current_date.month, current_date.day + timedelta, 23, 59
    )
else:
    due_date = datetime.today()

answer: str = None
file_type = None
while answer not in ["Y", "YES"]:
    file_type = input("File type: ")
    if file_type:
        answer = input("Are you sure? [yes, no]: ").upper()

with open("goal.txt", "w") as f:
    f.write(goal + "\n")
    f.write(due_date.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    f.write(file_type + "\n")
    print(
        f"Goal and deadline saved! Deadline is {due_date.strftime('%A, %B %d, %Y at %I:%M %p')} | File type: {file_type}"
    )

os.system("python checker.py")
