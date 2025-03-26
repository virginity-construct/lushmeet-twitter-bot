#!/usr/bin/env python3
"""
GitHub Actions runner for LushMeet Twitter Bot
This script is designed to be run by GitHub Actions on a schedule.
It runs one iteration of the bot's main loop.
"""

from main import LushMeetTwitterBot
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("lushmeet_bot_github_action")

if __name__ == "__main__":
    logger.info("Starting LushMeet Twitter Bot (GitHub Actions mode)...")
    
    # Create and run the bot once
    bot = LushMeetTwitterBot()
    
    # Run one iteration of the bot's main loop
    # You can enable follows and DMs by setting these to True
    bot.run_once(enable_follows=False, enable_dms=False)
    
    logger.info("Bot execution completed")
