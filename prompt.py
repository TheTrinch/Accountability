import os
from datetime import datetime

def set_goal():
    if os.path.exists('goal.txt'):
        with open('goal.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) > 1:
                deadline_str = lines[1].strip()
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
                if deadline > datetime.now():
                    print("Wait until the first goal is complete...")
                    return

    goal = input("Enter your goal: ")

    days = {"SUN":6, "MON":0, "TUE":1, "WED":2, "THU":3, "FRI":4, "SAT":5}
    deadline = None
    while deadline not in days:
        deadline = input("Enter deadline day [SUN, MON, TUE, WED, THU, FRI, SAT]: ").upper()
        if deadline not in days:
            print("Invalid day. Try again.")

    current_date = datetime.today()
    timedelta = days[deadline] - current_date.weekday()
    if timedelta <= 0:
        timedelta += 7
    due_date = datetime(current_date.year, current_date.month, current_date.day + timedelta, 23, 59)

    with open("goal.txt", "w") as f:
        f.write(goal + "\n")
        f.write(due_date.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        print(f"Goal and deadline saved! Deadline is {due_date.strftime('%A, %B %d, %Y at %I:%M %p')}")
set_goal()