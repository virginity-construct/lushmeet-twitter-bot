#!/usr/bin/env python3
"""
Test script to post a tweet using Twitter API v2 with OAuth 1.0a user context
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
logger = logging.getLogger("lushmeet_v2_test")

# Load environment variables
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def test_v2_tweet():
    """Test posting a tweet using Twitter API v2"""
    print("\n=== Testing Tweet Posting for @LushMeet ===\n")
    
    try:
        # Initialize Twitter API v2 client with OAuth 1.0a credentials
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_SECRET
        )
        
        # Get user information
        print("Retrieving user information...")
        me = client.get_me()
        
        if me.data:
            print(f"✅ Successfully authenticated as: @{me.data.username}")
            print(f"Account ID: {me.data.id}")
            
            # Ask for confirmation before posting
            tweet_text = "Testing LushMeet's exclusive Twitter presence. Private. Unapologetic. Untouchable. [Test]"
            
            print(f"\nReady to post this test tweet:")
            print(f"---\n{tweet_text}\n---")
            
            confirm = input("Do you want to post this tweet? (y/n): ")
            
            if confirm.lower() == 'y':
                print("\nPosting tweet...")
                response = client.create_tweet(text=tweet_text)
                
                if response.data:
                    tweet_id = response.data['id']
                    print(f"✅ Successfully posted tweet (ID: {tweet_id})")
                    print(f"View at: https://twitter.com/i/web/status/{tweet_id}")
                    return True
                else:
                    print("❌ Failed to post tweet - no data returned")
                    return False
            else:
                print("Tweet posting cancelled by user")
                return True
        else:
            print("❌ Failed to retrieve user information")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
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
        test_v2_tweet()
