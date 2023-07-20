#!/bin/bash

# Path to your Python script
PYTHON_SCRIPT="/home/juan/Desktop/llms/twitter-bot/blog.py"

# Write out current crontab
crontab -l > mycron

# Check whether PYTHON_SCRIPT is already scheduled
if grep -q "$PYTHON_SCRIPT" mycron; then
    echo "The script is already scheduled"
else
    # Echo new cron into cron file
    echo "0 7 * * * /usr/bin/python3 $PYTHON_SCRIPT" >> mycron
    # Install new cron file
    crontab mycron
    echo "The script was added to the cron jobs"
fi

# Remove the mycron file
rm mycron
