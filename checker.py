import os
from time import sleep
from threading import Thread
from datetime import datetime

import tkinter as tk
from tkinter import filedialog

running = False

def give_penalty():
    """
    Restrict access to any application or website the user picks.
    and notify them that the penalties will be activated
    """
    print("THERE WILL BE CONSEQUENCES")

def give_congrats(goal):
    """Give the user a notification that all checks have passed and allow them to select another goal"""
    print(f"Congrats! You achieved your goal: {goal}")
    os.system("python prompt.py")

def check_path(goal, filetype, folder_path):
    if check_folder(folder_path, filetype):
        give_congrats(goal)
    else:
        give_penalty()

def check_folder(path, filetype):
    if not path or not os.path.isdir(path):
        print("Invalid directory...")
        return False

    now = datetime.now()
    one_week_seconds = 7 * 24 * 60 * 60
    seconds_in_day = 60 * 60 * 24

    found_young = False
    found_any = False

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(f".{filetype.lower()}"):
                found_any = True
                try:
                    mtime = os.path.getmtime(file_path)
                    age = int((now - datetime.fromtimestamp(mtime)).total_seconds() // seconds_in_day)
                    print(f"File: {file} > Age: {age} days")
                    if (now - datetime.fromtimestamp(mtime)).total_seconds() <= one_week_seconds:
                        found_young = True
                except Exception as e:
                    print(f"Failed to open file: {e}")

    if not found_any:
        print(f"No .{filetype} files found in the directory.")
        give_penalty()
        return False

    return found_young

def check_goal(goal, deadline, file_type, folder_path):
    while running:
        if datetime.now() >= deadline:
            check_path(goal, file_type, folder_path)
            break
        sleep(5)

def load_goal_and_deadline():
    try:
        with open("goal.txt", "r") as f:
            lines = f.readlines()
            goal = lines[0].strip()
            deadline_str = lines[1].strip()
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
            file_type = lines[2].strip()
            return goal, deadline, file_type
    except Exception as e:
        print(f"Could not load goal and deadline: {e}")
        return None, None, None

if __name__ == "__main__":

    window = tk.Tk()
    window.withdraw()
    submit_dir = filedialog.askdirectory()
    window.destroy()
    
    if not submit_dir:
        print("No directory selected.")
        exit(1)
    
    goal, due_date, file_type = load_goal_and_deadline()
    if not goal or not due_date or not file_type:
        print("Goal, deadline, or file type not set. Please run the prompt script first.")
        exit(1)

    print(f"Submission Directory: {submit_dir}")
    print(f"File Type: {file_type}")
    print(f"Due: {due_date.strftime('%A, %B %d, %Y at %I:%M %p')}")
    print(f"Goal: {goal}")

    running = True
    thread = Thread(target=check_goal, args=(goal, due_date, file_type, submit_dir))
    thread.start()