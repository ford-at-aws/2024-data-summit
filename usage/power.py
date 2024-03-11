import subprocess
from datetime import datetime, timedelta
import re
import argparse

# Parse arguments for debug mode
parser = argparse.ArgumentParser(description='Calculate total wake time from log with optional debug output.')
parser.add_argument('--debug', action='store_true', help='Enable debug logging')
args = parser.parse_args()


def debug_log(message):
    if args.debug:
        print(f'DEBUG: {message}')


# Function to fetch the power log using a subprocess
def fetch_power_log():
    debug_log('Fetching power log...')
    subprocess.run(["pmset", "-g", "log", "|", "grep", "WakeTime\|Entering Sleep", ">", "power.log"], capture_output=True)


# Function to parse a line in the log file
def parse_line(line):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) -0500 (\w+)'
    match = re.search(pattern, line)
    if match:
        timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
        event = match.group(2)
        return timestamp, event
    return None, None


# Function to calculate wake times
def calculate_wake_times():
    fetch_power_log()  # Call the function to create/update the power.log file
    log_file_path = 'power.log'
    wake_periods = {}

    with open(log_file_path, 'r') as file:
        wake_start = None
        for line in file:
            timestamp, event = parse_line(line)
            if timestamp is not None:
                date = timestamp.date()
                if event == 'WakeTime' and wake_start is None:
                    wake_start = timestamp
                    debug_log(f'Start wake period: {wake_start}')
                elif event == 'Sleep' and wake_start is not None:
                    duration = timestamp - wake_start
                    if date not in wake_periods:
                        wake_periods[date] = [duration]
                    else:
                        wake_periods[date].append(duration)
                    debug_log(f'End wake period: {timestamp}, Duration: {duration}')
                    wake_start = None

    # Sum up durations for each day and convert to a readable format
    wake_times_summed = {}
    for date, durations in wake_periods.items():
        total_duration = sum(durations, timedelta())
        total_seconds = total_duration.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        wake_times_summed[date] = f'{int(hours)}h {int(minutes)}m'
        print(f'Date: {date}, Total Wake Time: {wake_times_summed[date]}')

    return wake_times_summed


if __name__ == "__main__":
    calculate_wake_times()
