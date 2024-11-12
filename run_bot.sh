#!/bin/bash
echo "Starting Telegram Bot..."

# Debug information
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found! Please run activate.sh first."
    exit 1
fi

# Check if bot.py exists
if [ ! -f "bot.py" ]; then
    echo "Error: bot.py not found!"
    exit 1
fi

# Run the bot
python3 bot.py

# If bot crashes or stops, wait for user input
read -p "Press Enter to continue..."