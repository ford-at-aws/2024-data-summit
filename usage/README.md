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
