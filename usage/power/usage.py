# Import necessary libraries
import argparse
import logging

# Set up the argument parser to accept a --debug flag
parser = argparse.ArgumentParser(
    description="Extract and display the total energy usage from a snapshot file."
)
parser.add_argument("file_path", type=str, help="The path to the snapshot file.")
parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
args = parser.parse_args()

# Configure logging based on the --debug flag
if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


# Define a function to extract the total energy usage with added debug logging
def extract_total_energy_usage(file_path):
    logging.debug(f"Opening file: {file_path}")

    combined_power = 0

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            logging.debug("File read successfully.")

        for line in lines:
            if "Combined Power" in line:
                combined_power = float(line.split(":")[1].strip().split(" ")[0])
                logging.debug(f"Combined Power found: {combined_power} mW")
                break
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

    return combined_power


# Main execution
if __name__ == "__main__":
    total_energy_usage = extract_total_energy_usage(args.file_path)
    if total_energy_usage is not None:
        print(f"Total Energy Usage: {total_energy_usage} mW")
    else:
        print("Could not extract total energy usage.")
