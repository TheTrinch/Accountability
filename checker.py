# Standard library imports
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta
from time import sleep
from threading import Thread

# Third-party imports
import tkinter as tk
from tkinter import filedialog

# --- Constants ---
GOAL_FILE = "goal.txt"
REMINDER_FILE = "MISSED_GOAL_REMINDER.txt"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# --- Global State ---
running = False

# --- Penalty Definitions ---
PENALTIES = [
    "reflection_time",
    "chore_task",
    "reminder_file",
    "stern_message"
]

# --- Helper Functions ---

def _load_goal_details():
    """
    Safely reads the current goal text, deadline datetime object, and file type
    from the GOAL_FILE.
    Returns (goal, deadline, file_type) or (None, None, None) on error.
    """
    try:
        with open(GOAL_FILE, "r") as f:
            lines = [line.strip() for line in f if line.strip()] # Read non-empty lines and strip whitespace
            
            if len(lines) < 3:
                # Provide more detail on what was found if fewer lines than expected
                raise ValueError(
                    f"'{GOAL_FILE}' is malformed. Expected 3 non-empty lines "
                    f"(goal, deadline, file_type), but found {len(lines)}."
                )
            
            goal = lines[0]
            deadline_str = lines[1]
            deadline = datetime.strptime(deadline_str, DATETIME_FORMAT)
            file_type = lines[2]
            return goal, deadline, file_type
    except FileNotFoundError:
        print(f"ERROR: Goal file '{GOAL_FILE}' not found. Please run the prompt script first to set a goal.")
    except (ValueError, IndexError) as e:
        print(
            f"ERROR: Failed to parse '{GOAL_FILE}'. Please ensure its format is correct "
            f"(goal on line 1, deadline '{DATETIME_FORMAT}' on line 2, file type on line 3). "
            f"Details: {e}"
        )
    except Exception as e:
        # Catch any other unexpected errors during file reading
        print(f"An unexpected error occurred while reading '{GOAL_FILE}': {e}")
    return None, None, None

def give_penalty():
    """
    Selects a random penalty type and executes the corresponding action.
    Prints a descriptive message to the user.
    """
    print("\n" + "="*50)
    print("          GOAL MISSED! PENALTY ISSUED          ")
    print("="*50)

    selected_penalty_type = random.choice(PENALTIES)
    print(f"Penalty Type: {selected_penalty_type.replace('_', ' ').upper()}\n")

    if selected_penalty_type == "reflection_time":
        print("Take some time to reflect on why this goal was missed.")
        print("Consider setting a new, more achievable goal or adjusting your strategy.")
        print("Perhaps write down a few paragraphs about what went wrong and how you can improve.")
    elif selected_penalty_type == "chore_task":
        print("As a consequence of missing your goal, you are assigned a chore task.")
        print("Go clean something that needs cleaning in your living space "
              "(e.g., wash dishes, vacuum, wipe surfaces).")
        print("This helps reinforce the idea that responsibilities have consequences.")
    elif selected_penalty_type == "reminder_file":
        print(f"A reminder file detailing your missed goal ({REMINDER_FILE}) has been created.")
        # Use the consolidated loader to get goal details for the reminder file
        goal_text, deadline_dt, _ = _load_goal_details() 
        if goal_text and deadline_dt:
            try:
                with open(REMINDER_FILE, "w") as f:
                    f.write("--- MISSED GOAL REMINDER ---\n")
                    f.write(f"You missed your goal:\n'{goal_text}'\n")
                    f.write(f"The deadline was: {deadline_dt.strftime('%A, %B %d, %Y at %I:%M %p')}\n\n")
                    f.write("Take this as a reminder to stay focused on your commitments.\n")
                    f.write("Reflect on what led to this outcome and how you can avoid it in the future.\n")
                print(f"Check '{REMINDER_FILE}' in the current directory for details.")
            except IOError as e:
                print(f"ERROR: Could not create '{REMINDER_FILE}': {e}")
        else:
            print("WARNING: Could not retrieve goal details to create the reminder file due to previous errors.")
    elif selected_penalty_type == "stern_message":
        print("This is a stern reminder: You committed to a goal and failed to achieve it.")
        print("Your time is valuable. Your commitments matter. Do not let this happen again.")
        print("Re-evaluate your priorities and dedication.")
    else:
        # Fallback for unexpected penalty types, though random.choice prevents this with a fixed list.
        print("An unknown penalty type was selected. Defaulting to a general warning.")
        print("You missed your goal. Better luck next time!")

    print("\n" + "="*50)
    print("        End of Penalty - Time to Re-focus        ")
    print("="*50 + "\n")

def give_congrats(goal):
    """
    Prints a congratulatory message and attempts to restart the goal-setting process.
    """
    print(f"Congrats! You achieved your goal: '{goal}'")
    try:
        # Use subprocess.run for more robust execution of external Python scripts.
        # sys.executable ensures the correct Python interpreter is used.
        # check=True will raise CalledProcessError if prompt.py exits with non-zero.
        # capture_output=False means it inherits the parent's stdout/stderr, showing prompt.py's output.
        print("\nStarting new goal setup...\n")
        subprocess.run([sys.executable, "prompt.py"], check=True, capture_output=False)
    except FileNotFoundError:
        print("WARNING: 'prompt.py' not found. Cannot restart goal setting.")
    except subprocess.CalledProcessError as e:
        print(f"WARNING: 'prompt.py' exited with an error. Please check its execution. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while trying to run 'prompt.py': {e}")

def check_path(goal, filetype, folder_path):
    """
    Checks the specified folder for files matching the criteria.
    Gives congratulations if goal is met, otherwise a penalty.
    """
    # The check_folder function already calls give_penalty if no files or young files are found.
    # So, if check_folder returns True, it means a young file was found and the goal is met.
    if check_folder(folder_path, filetype):
        give_congrats(goal)
    # The 'else' (penalty) is handled within check_folder if it returns False.

def check_folder(path, filetype):
    """
    Recursively checks a directory for files of a specific type modified within the last week.
    Returns True if a qualifying file is found, False otherwise.
    Also issues a penalty if no relevant files are found.
    """
    if not path or not os.path.isdir(path):
        print(f"ERROR: Invalid directory provided for checking: '{path}'. Cannot verify goal completion.")
        give_penalty() # Give penalty if directory itself is invalid
        return False

    now = datetime.now()
    one_week_ago = now - timedelta(weeks=1)
    
    found_young = False
    found_any = False

    # Normalize filetype to be case-insensitive for robust matching.
    # The plan implies filetype without a dot (e.g., "txt"), so prepend it here.
    target_extension = f".{filetype.lower()}" 

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            # Ensure case-insensitive check for file extension
            if file.lower().endswith(target_extension):
                found_any = True
                try:
                    mtime = os.path.getmtime(file_path)
                    file_datetime = datetime.fromtimestamp(mtime)
                    
                    # Calculate age in days for display (optional, but good for context)
                    age_days = (now - file_datetime).days
                    print(f"File: '{file}' (Path: '{file_path}') > Modified: {file_datetime.strftime(DATETIME_FORMAT)} (Age: {age_days} days)")
                    
                    # Check if file modification time is within the last week
                    if file_datetime >= one_week_ago:
                        found_young = True
                except OSError as e: # Catch specific OS errors for file access (e.g., permission denied)
                    print(f"WARNING: Failed to get modification time for '{file_path}': {e}")
                except Exception as e: # Catch any other unexpected errors during file processing
                    print(f"WARNING: An unexpected error occurred while processing file '{file_path}': {e}")

    if not found_any:
        print(f"No '{target_extension}' files found in the directory '{path}' or its subdirectories.")
        give_penalty()
        return False

    if not found_young:
        print(f"No '{target_extension}' files modified within the last week found in '{path}'.")
        give_penalty() # Give penalty if no young files are found
        return False

    return found_young # If we reach here, found_young must be True.

def check_goal(goal, deadline, file_type, folder_path):
    """
    Monitors the current time against the goal's deadline.
    Once the deadline is reached, it triggers the goal verification process.
    """
    global running # Declare intent to modify the global 'running' flag
    while running:
        if datetime.now() >= deadline:
            print(f"\n--- Deadline ({deadline.strftime(DATETIME_FORMAT)}) reached for goal: '{goal}' ---")
            check_path(goal, file_type, folder_path)
            running = False # Signal the thread to stop after completing the check
            break
        sleep(5) # Check every 5 seconds to avoid busy-waiting

# --- Main Execution ---
if __name__ == "__main__":
    # Initialize Tkinter for file dialog, then immediately hide it.
    # This prevents an empty Tkinter window from appearing unnecessarily.
    window = tk.Tk()
    window.withdraw()
    
    submit_dir = filedialog.askdirectory(title="Select your submission directory")
    window.destroy() # Destroy the Tkinter window after selection

    if not submit_dir:
        print("No directory selected. Exiting.")
        sys.exit(1) # Use sys.exit for a clean program termination

    # Load goal details using the single, consolidated helper function
    goal, due_date, file_type = _load_goal_details()
    if not goal or not due_date or not file_type:
        print("Cannot proceed without a valid goal, deadline, and file type. "
              "Please ensure 'goal.txt' is correctly set up.")
        sys.exit(1)

    print("\n" + "="*50)
    print("          GOAL TRACKER INITIATED          ")
    print("="*50)
    print(f"Submission Directory: '{submit_dir}'")
    print(f"Expected File Type: '{file_type}'")
    print(f"Goal Deadline: {due_date.strftime('%A, %B %d, %Y at %I:%M %p')}")
    print(f"Goal: '{goal}'")
    print("Monitoring for deadline...")
    print("="*50 + "\n")

    running = True
    # Create a new thread to run the goal checking in the background
    thread = Thread(target=check_goal, args=(goal, due_date, file_type, submit_dir))
    thread.start()

    # The main thread waits for the background thread to complete its task.
    # This ensures that the program does not exit prematurely while the goal
    # is still being monitored or while penalty/congrats messages are being processed.
    thread.join()
    print("\nGoal monitoring finished. Program exiting.")