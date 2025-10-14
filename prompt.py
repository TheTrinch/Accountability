from datetime import datetime

def set_goal():
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
    due_date = datetime(current_date.year, current_date.month, current_date.day, 23, 59) + timedelta * timedelta.__class__(days=1)

    with open("goal.txt", "w") as f:
        f.write(goal + "\n")
        f.write(due_date.strftime("%Y-%m-%d %H:%M:%S") + "\n")

    print(f"Goal and deadline saved! Deadline is {due_date.strftime('%A, %B %d, %Y at %I:%M %p')}")