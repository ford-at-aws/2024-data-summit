# About this script
This script prints a snapshot of your laptop's energy usage for 1 second.

# Run it
`python3 usage.py` with `--debug` for extra logging.

Results are saved to a local text file.

## Usage
This script is designed to run via cron.

1. Run `sudo visudo` to edit sudoers file to add:
```
your_username ALL=(ALL) NOPASSWD: /usr/bin/powermetrics
```
3. Set up cron, run `crontab -e` and add:
```
*/10 * * * * /usr/bin/python3 /path/to/your_script.py
```

# Note
Only tested on MacOS Sonoma.

---

# For nerds
### Power Measurement
The script initially measures power in milliwatts (mW) as provided by the powermetrics output, which indicates the instantaneous power usage of the system (CPU, GPU, ANE combined).

### Energy Calculation
To calculate energy usage, the script multiplies this power usage (converted to kilowatts by dividing by 1,000,000 to convert mW to kW) by the duration for which the power is used (in hours). The formula used is Energy (kWh) = Power (kW) × Time (hours). This gives the total energy used over the specified period in kilowatt-hours (kWh).

### What kWh Represents
A kilowatt-hour is a measure of energy that represents the amount of energy used if a 1,000-watt appliance runs for an hour. In your script's context, it reflects the total energy consumption of your system's components (CPU, GPU, ANE) over the specified duration. It's a cumulative measure, meaning if your system consistently used 1 kW of power over the specified period, and you ran the script with the period set to 1 hour, it would report an energy usage of 1 kWh.
