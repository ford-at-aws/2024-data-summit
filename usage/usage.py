import subprocess
import re
import argparse
from datetime import datetime

def get_powermetrics_output():
    command = ["sudo", "powermetrics", "-i", "5000", "-n", "1"]
    try:
        output = subprocess.check_output(command, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error executing powermetrics: {e}"

def extract_combined_power_usage(powermetrics_output):
    power_usage_pattern = re.compile(r'Combined Power \(CPU \+ GPU \+ ANE\): (\d+) mW')
    matches = power_usage_pattern.findall(powermetrics_output)
    return sum(int(match) for match in matches) if matches else 0

def log_energy_usage(hours, energy_usage_kWh, per_hour_energy_usage_kWh):
    with open("~/energy_usage_log.txt", "a") as log_file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{current_time} - Total Energy Usage for {hours} hours: {energy_usage_kWh} kWh\n")
        log_file.write(f"{current_time} - Energy Usage per Hour: {per_hour_energy_usage_kWh} kWh\n\n")

if __name__ == "__main__":
    hours = 24  # Default to 24 hours, adjust if needed
    seconds = hours * 3600
    powermetrics_output = get_powermetrics_output()
    if powermetrics_output and not powermetrics_output.startswith("Error"):
        total_power_usage = extract_combined_power_usage(powermetrics_output)
        energy_usage_kWh = (total_power_usage / 1000000) * seconds / 3600
        per_hour_energy_usage_kWh = energy_usage_kWh / hours
        log_energy_usage(hours, energy_usage_kWh, per_hour_energy_usage_kWh)
    else:
        print(powermetrics_output)
