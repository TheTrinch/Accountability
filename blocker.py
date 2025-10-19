import psutil
import time
import platform
import os


def is_windows() -> bool:
    return platform.system() == "Windows"


PROGRAMS = [
    "discord",
]

# Add a .exe to each process if the script is running on Windows
BLACKLIST = [program + ".exe" if is_windows() else program for program in PROGRAMS]


def kill_processes():
    """
    Continuously scans for and terminates blacklisted processes.
    """
    while True:
        for proc in psutil.process_iter(["name"]):
            # Check if the current process is the list of blacklisted processes
            if proc.info["name"].lower() in [p.lower() for p in BLACKLIST]:
                try:
                    proc.kill()
                    print(f"Terminated: {proc.info['name']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    print(f"Could not terminate {proc.info['name']}: {e}")
        # Avoid using too much CPU usage
        kill_delay = os.environ["KILL_DELAY"]
        if kill_delay is not None:
            time.sleep(int(kill_delay))
        else:
            time.sleep(1)


if __name__ == "__main__":
    print("Starting blocker...")
    print(f"Blacklisted applications: {', '.join(BLACKLIST)}")
    kill_processes()
