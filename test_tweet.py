#!/usr/bin/env python3
"""
Test script to post a tweet to the @LushMeet Twitter account
"""

import os
import tweepy
from dotenv import load_dotenv
import logging
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("lushmeet_bot_test_tweet")

# Load environment variables
load_dotenv()

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def load_tweets():
    """Load tweets from tweets.txt"""
    try:
        with open("tweets.txt", 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Error loading tweets: {e}")
        return ["Test tweet from LushMeet. Private. Unapologetic. Untouchable. 💎"]

def post_test_tweet():
    """Post a test tweet to verify write permissions"""
    try:
        # Initialize Twitter API v2 client
        client_v2 = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET
        )
        
        # Get a random tweet from the tweets.txt file
        tweets = load_tweets()
        tweet_text = random.choice(tweets)
        
        # Add a test indicator (remove this in production)
        tweet_text = f"{tweet_text} [Test]"
        
        # Post the tweet
        response = client_v2.create_tweet(text=tweet_text)
        
        if response.data:
            tweet_id = response.data['id']
            logger.info(f"Successfully posted test tweet (ID: {tweet_id})")
            logger.info(f"Tweet content: {tweet_text}")
            logger.info(f"View at: https://twitter.com/LushMeet/status/{tweet_id}")
            return True
        else:
            logger.error("Failed to post tweet")
            return False
    
    except Exception as e:
        logger.error(f"Error posting tweet: {e}")
        return False

if __name__ == "__main__":
    # Check if required environment variables are set
    missing_vars = []
    for var in ["TWITTER_API_KEY", "TWITTER_API_SECRET", "TWITTER_ACCESS_TOKEN", 
                "TWITTER_ACCESS_SECRET", "TWITTER_BEARER_TOKEN"]:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in the .env file")
        exit(1)
    
    # Ask for confirmation before posting
    print("This script will post a test tweet to the @LushMeet account.")
    confirm = input("Do you want to continue? (y/n): ")
    
    if confirm.lower() == 'y':
        # Post test tweet
        if post_test_tweet():
            logger.info("Test tweet posted successfully! The bot is ready to use with @LushMeet")
        else:
            logger.error("Failed to post test tweet. Please check your credentials and try again")
    else:
        logger.info("Test canceled by user")
