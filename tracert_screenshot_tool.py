import os
import subprocess
import argparse
import pyautogui
import time
from datetime import datetime

# Define color codes for console output
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END_FORMAT = "\033[0m"

# Define the output folder for screenshots and tracert logs
output_folder = "tracert_results"

def clear_console():
    try:
        # Clear the console screen based on the operating system
        os.system('clear' if os.name == 'posix' else 'cls')
    except Exception as e:
        print("Error clearing the console:", e)

def run_tracert(host):
    try:
        # Run the tracert command and capture the output
        tracert_command = ["tracert", host]
        output = subprocess.check_output(tracert_command, stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return str(e.output)

def capture_screenshot(filename):
    try:
        # Delay to ensure the console output is visible
        time.sleep(1)

        # Capture the entire screen and save the screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print("Error capturing screenshot:", e)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="tracert targets from a list and capture screenshots.")
    parser.add_argument("-f", "--file", required=True, help="File containing a list of host names or IP addresses")
    args = parser.parse_args()

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Read the list of host names or IP addresses from the file
    with open(args.file, "r") as file:
        host_list = file.read().splitlines()

    print("tracert results:")
    clear_console()

    # tracert each target, capture a screenshot, and save the tracert log
    for idx, host in enumerate(host_list, start=1):  # Use enumerate with start to improve readability
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Current time: {current_time}")
            print(f"\n{COLOR_GREEN}Target {idx}/{len(host_list)}: {host}{COLOR_RESET}")
            tracert_result = run_tracert(host)

            print(f"\nResult:")
            formatted_tracert_result = "\n".join([f"{COLOR_RED}{line}{COLOR_RESET}" for line in tracert_result.split("\n")])
            print(formatted_tracert_result)

            log_filename = os.path.join(output_folder, f"tracert_log_{idx}.txt")
            with open(log_filename, "w") as log_file:
                log_file.write(tracert_result)

            screenshot_filename = os.path.join(output_folder, f"tracert_screenshot_{idx}.png")
            capture_screenshot(screenshot_filename)

        except Exception as e:
            print("Error processing target:", e)
        
        clear_console()

if __name__ == "__main__":
    main()
