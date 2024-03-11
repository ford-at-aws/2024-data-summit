import subprocess
import re
import os
from datetime import datetime

def get_powermetrics_output(duration=1000):
    command = ["sudo", "powermetrics", "-i", f"{duration}", "-n", "1"]
    dir_path = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(dir_path, "powermetrics_logs")
    os.makedirs(logs_dir, exist_ok=True)  # Ensure the directory exists
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"powermetrics_output_{current_time}.txt"
    log_file_path = os.path.join(logs_dir, log_file_name)

    try:
        output = subprocess.check_output(command, text=True)
        with open(log_file_path, "w") as log_file:  # Write to a unique timestamp log file
            log_file.write(output)
        return output
    except subprocess.CalledProcessError as e:
        error_message = f"Error executing powermetrics: {e}"
        with open(log_file_path, "w") as log_file:  # Write error to the same unique timestamp log file
            log_file.write(error_message)
        return error_message

def extract_combined_power_usage(powermetrics_output):
    power_usage_pattern = re.compile(r'Combined Power \(CPU \+ GPU \+ ANE\): (\d+) mW')
    matches = power_usage_pattern.findall(powermetrics_output)
    return sum(int(match) for match in matches) if matches else 0

def log_energy_usage(hours, energy_usage_kWh, per_hour_energy_usage_kWh, total_power_usage, duration):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(dir_path, "energy_usage_log.txt")
    with open(log_file_path, "a") as log_file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{current_time} - Total Energy Consumption for {duration} ms: {total_power_usage} mW\n")
        log_file.write(f"{current_time} - Energy Usage: {per_hour_energy_usage_kWh} kWh\n")
        log_file.write(f"{current_time} - Example Energy Usage for {hours} hours: {energy_usage_kWh} kW\n\n")


if __name__ == "__main__":
    hours = 24  # Default to 24 hours, adjust if needed
    seconds = hours * 3600
    powermetrics_output = get_powermetrics_output()
    if powermetrics_output and not powermetrics_output.startswith("Error"):
        total_power_usage = extract_combined_power_usage(powermetrics_output)
        energy_usage_kWh = (total_power_usage / 1000000) * seconds / 3600
        per_hour_energy_usage_kWh = energy_usage_kWh / hours
        log_energy_usage(hours, energy_usage_kWh, per_hour_energy_usage_kWh, total_power_usage, 1000)
    else:
        print(powermetrics_output)
