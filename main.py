"""
Authenticity is a CLI application that gives you penalties for not hitting your goal.

Implemented
------------

* Setting a goal
* Setting a deadline

TODO
-----

* Penalties
* Checking Goal
* Giving Congrats
* Create Logs

"""

import os
import tkinter
from time import sleep
from threading import Thread
from datetime import datetime

running = False
days = {"SUN":6, "MON":0, "TUE":1, "WED":2, "THU":3, "FRI":4, "SAT":5}

def give_penalty():
    pass

def give_congrats(goal, deadline):
    pass

def check_path(path, filetype):
    
    pass

def check_goal(deadline, path, filetype):

    while running:
        if datetime.now() >= deadline:
            check_path(path, filetype)
            break
        sleep(5)

def set_deadline(deadline):

    current_date = datetime.today()
    timedelta = days[deadline] - current_date.weekday()
    if timedelta <= 0:
        timedelta += 7
    return datetime(current_date.year, current_date.month, (timedelta + current_date.day), 23, 59)

def prompt(question):

    value = NotImplemented
    answer = NotImplemented
    while not answer == 'yes':
        value = input(question)
        answer = input("Are you sure? [yes, no]")
    return value

if __name__ == "__main__":
    pass
"""
if __name__ == "__main__":

    goal = prompt("Goal: ")
    
    try:
        submit_dir = prompt("Submission Directory: ")
        if not os.path.isdir(submit_dir):
            raise NotADirectoryError
    except NotADirectoryError:
        print("This directory is invalid...")

    filetype = prompt("File Type: ")
    
    deadline = NotImplemented
    while deadline not in days:
        deadline = input("Deadline [SUN-SAT]: ");
        
        if deadline not in days:
            print("Try again.")

    due_date = set_deadline(deadline)
    
    print(f"Goal: {goal}")
    print(f"Submission Directory: {submit_dir}")
    print(f"File Type: {filetype}")
    print(f"Due: {due_date.strftime("%x %I:%M %p")}")

    running = True
    thread = Thread(target=check_goal, args=(due_date, submit_dir, filetype))
    thread.start()
"""