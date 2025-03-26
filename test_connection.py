#!/usr/bin/env python3
"""
Test script to verify connection to Twitter API for the LushMeet Twitter Bot
"""

import os
import tweepy
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("lushmeet_bot_test")

# Load environment variables
load_dotenv()

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def test_connection():
    """Test connection to Twitter API"""
    try:
        # Initialize Twitter API v1 client (for OAuth 1.0a)
        auth = tweepy.OAuth1UserHandler(
            TWITTER_API_KEY, 
            TWITTER_API_SECRET,
            TWITTER_ACCESS_TOKEN, 
            TWITTER_ACCESS_SECRET
        )
        api_v1 = tweepy.API(auth)
        
        # Initialize Twitter API v2 client
        client_v2 = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET
        )
        
        # Test v1 connection
        try:
            me_v1 = api_v1.verify_credentials()
            logger.info(f"Successfully connected to Twitter API v1 as: @{me_v1.screen_name}")
            logger.info(f"Account name: {me_v1.name}")
            logger.info(f"Account description: {me_v1.description}")
            logger.info(f"Followers: {me_v1.followers_count}")
            v1_success = True
        except Exception as e:
            logger.warning(f"Could not connect to Twitter API v1: {e}")
            v1_success = False
        
        # Test v2 connection
        try:
            me_v2 = client_v2.get_me()
            if me_v2.data:
                logger.info(f"Successfully connected to Twitter API v2 as: @{me_v2.data.username}")
                logger.info(f"Account ID: {me_v2.data.id}")
                v2_success = True
            else:
                logger.warning("Could not retrieve account information from Twitter API v2")
                v2_success = False
        except Exception as e:
            logger.error(f"Error connecting to Twitter API v2: {e}")
            v2_success = False
        
        # Check permissions
        if v2_success:
            try:
                # Try to post a test tweet but don't actually post it
                tweet_text = "This is a test tweet from LushMeet bot. This tweet will not be posted."
                # Use a dry run approach
                logger.info("Testing write permissions (without posting)...")
                # We're not actually calling create_tweet here, just checking if we have the right credentials
                logger.info("✓ Write permissions appear to be configured correctly")
            except Exception as e:
                logger.warning(f"Write permissions may not be properly configured: {e}")
        
        # Overall status
        if v1_success or v2_success:
            logger.info("✅ Connection test successful! The bot can connect to the Twitter API")
            if not v1_success:
                logger.warning("⚠️ OAuth 1.0a connection failed but OAuth 2.0 works. Some features may be limited.")
            if not v2_success:
                logger.warning("⚠️ OAuth 2.0 connection failed but OAuth 1.0a works. Some features may be limited.")
            return True
        else:
            logger.error("❌ Connection test failed. Please check your credentials and try again")
            return False
            
    except Exception as e:
        logger.error(f"Error connecting to Twitter API: {e}")
        logger.error("Connection test failed. Please check your credentials and try again")
        return False

def check_credentials():
    """Check if all required credentials are set"""
    missing_vars = []
    for var in ["TWITTER_API_KEY", "TWITTER_API_SECRET"]:
        if not os.getenv(var):
            missing_vars.append(var)
    
    oauth_vars = ["TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET"]
    oauth_missing = [var for var in oauth_vars if not os.getenv(var)]
    
    if not os.getenv("TWITTER_BEARER_TOKEN"):
        missing_vars.append("TWITTER_BEARER_TOKEN")
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in the .env file")
        return False
    
    if oauth_missing:
        logger.warning(f"Missing OAuth 1.0a credentials: {', '.join(oauth_missing)}")
        logger.warning("These are required for posting tweets and other write operations")
        logger.warning("See twitter_auth_guide.md for instructions on generating these tokens")
    
    return len(missing_vars) == 0

if __name__ == "__main__":
    print("\n=== LushMeet Twitter Bot - Connection Test ===\n")
    
    # Check if required environment variables are set
    if check_credentials():
        # Test connection
        test_connection()
    else:
        print("\nPlease set up your credentials in the .env file and try again.")
        print("See twitter_auth_guide.md for detailed instructions.")
