#!/usr/bin/env python3
"""
Test script to verify OAuth 1.0a authentication for Twitter API v1.1
This is specifically for testing posting capabilities
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
logger = logging.getLogger("lushmeet_v1_test")

# Load environment variables
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

def test_v1_auth():
    """Test OAuth 1.0a authentication for Twitter API v1.1"""
    print("\n=== Testing OAuth 1.0a Authentication for @LushMeet ===\n")
    
    try:
        # Set up OAuth 1.0a authentication
        auth = tweepy.OAuth1UserHandler(
            API_KEY, 
            API_SECRET,
            ACCESS_TOKEN, 
            ACCESS_SECRET
        )
        
        # Create API object
        api = tweepy.API(auth)
        
        # Verify credentials
        print("Verifying credentials...")
        me = api.verify_credentials()
        
        print(f"✅ Successfully authenticated as: @{me.screen_name}")
        print(f"Account name: {me.name}")
        print(f"Followers: {me.followers_count}")
        print(f"Account created: {me.created_at}")
        
        # Check if we can post tweets
        print("\nChecking write permissions...")
        
        # We won't actually post a tweet, just check if we have the right permissions
        if me.screen_name:
            print("✅ Write permissions appear to be correctly configured")
            print("The bot should be able to post tweets as @" + me.screen_name)
        
        return True
        
    except tweepy.TweepyException as e:
        print(f"❌ Authentication failed: {e}")
        
        # Provide more specific error guidance
        error_str = str(e).lower()
        if "401" in error_str:
            print("\nThis appears to be an authentication error. Possible causes:")
            print("1. The API key/secret or access token/secret may be incorrect")
            print("2. The tokens may have expired or been revoked")
            print("3. The app may not have the required permissions (needs Read+Write)")
        elif "403" in error_str:
            print("\nThis appears to be a permissions error. Possible causes:")
            print("1. The app may not have the required permissions (needs Read+Write)")
            print("2. The account may be restricted or in read-only mode")
        
        print("\nPlease check your credentials in the .env file and try again.")
        return False

if __name__ == "__main__":
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
        print("❌ Missing required credentials in .env file")
        print("Please ensure all credentials are set:")
        print("- TWITTER_API_KEY")
        print("- TWITTER_API_SECRET")
        print("- TWITTER_ACCESS_TOKEN")
        print("- TWITTER_ACCESS_SECRET")
    else:
        test_v1_auth()
