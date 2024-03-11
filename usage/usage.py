import subprocess
import re
import argparse


def get_powermetrics_output():
    # Command to run (includes sudo, might require password input)
    command = ["sudo", "powermetrics", "-i", "1000", "-n", "1"]

    # Execute the command and capture its output
    try:
        output = subprocess.check_output(command, text=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing powermetrics: {e}")
        return ""


def extract_combined_power_usage(powermetrics_output):
    # Regular expression to find the Combined Power usage line
    power_usage_pattern = re.compile(r'Combined Power \(CPU \+ GPU \+ ANE\): (\d+) mW')

    # Search for the pattern in the powermetrics output
    matches = power_usage_pattern.findall(powermetrics_output)

    # Convert all found matches to integers and sum them
    if matches:
        power_usages = [int(match) for match in matches]
        return sum(power_usages)
    else:
        return 0


def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate total energy usage based on powermetrics output.')
    parser.add_argument('seconds', type=int, help='Duration in seconds to calculate energy usage for.')
    args = parser.parse_args()
    return args.seconds


# Main logic
if __name__ == "__main__":
    seconds = parse_arguments()
    powermetrics_output = get_powermetrics_output()
    if powermetrics_output:
        total_power_usage = extract_combined_power_usage(powermetrics_output)
        print(f'Total Combined Power Usage per Second: {total_power_usage} mW')
        energy_usage = total_power_usage * seconds
        print(f'Total Energy Usage for {seconds} seconds: {energy_usage} mWs (milliwatt-seconds)')
    else:
        print("Failed to get powermetrics data.")
