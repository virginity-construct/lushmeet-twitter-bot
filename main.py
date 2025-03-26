#!/usr/bin/env python3
"""
LushMeet Twitter Bot - Automated promotion for the LushMeet platform
Features:
- Scheduled promotional tweets
- Replies to trending niche tweets
- Optional follow/DM functionality
"""

import os
import json
import time
import random
import logging
import tweepy
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("lushmeet_bot")

# Constants
STATE_FILE = "bot_state.json"
TWEET_INTERVAL_HOURS = 4  # Post a tweet every 4 hours
REPLY_INTERVAL_MINUTES = 30  # Check for tweets to reply to every 30 minutes
MIN_LIKES_THRESHOLD = 2  # Minimum likes for a tweet to be worth replying to
FOLLOW_LIMIT_PER_DAY = 20  # Maximum follows per day
DM_LIMIT_PER_DAY = 5  # Maximum DMs per day

# Rate limiting constants
MAX_RETRIES = 5  # Maximum number of retries for API calls
INITIAL_BACKOFF = 60  # Initial backoff in seconds (1 minute)
MAX_BACKOFF = 3600  # Maximum backoff in seconds (1 hour)
RATE_LIMIT_RESET_BUFFER = 5  # Additional seconds to wait after rate limit reset

# Target hashtags for finding tweets to reply to
TARGET_HASHTAGS = [
    "#sugarbaby", "#escortlife", "#onlyfans", "#luxury", 
    "#GFE", "#companionship", "#sugardaddy", "#elitecompanion"
]


class LushMeetTwitterBot:
    """Twitter bot for promoting LushMeet platform"""
    
    def __init__(self):
        """Initialize the bot with Twitter API credentials and load state"""
        self.state = self._load_state()
        self._check_reset_daily_counters()
        
        # Initialize Twitter API clients
        self.client_v1 = self._init_v1_client()
        self.client_v2 = self._init_v2_client()
        
        # Load content
        self.tweets = self._load_content("tweets.txt")
        self.replies = self._load_content("replies.txt")
        self.dms = self._load_content("dms.txt")
        
        # Rate limit tracking
        self.rate_limits = {
            "search": {"remaining": 180, "reset_time": time.time()},
            "tweet": {"remaining": 200, "reset_time": time.time()},
            "follow": {"remaining": 50, "reset_time": time.time()},
            "dm": {"remaining": 200, "reset_time": time.time()}
        }
        
        logger.info("LushMeet Twitter Bot initialized")
    
    def _init_v1_client(self):
        """Initialize Twitter API v1.1 client (for some actions not in v2)"""
        auth = tweepy.OAuth1UserHandler(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET")
        )
        return tweepy.API(auth)
    
    def _init_v2_client(self):
        """Initialize Twitter API v2 client"""
        return tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
    
    def _load_state(self):
        """Load bot state from file or create default state"""
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading state file: {e}")
        
        # Default state
        return {
            "last_tweet_time": None,
            "last_reply_time": None,
            "tweets_posted_today": 0,
            "replies_sent_today": 0,
            "follows_today": 0,
            "dms_sent_today": 0,
            "last_reset_date": datetime.now().strftime("%Y-%m-%d"),
            "replied_to_tweets": [],
            "followed_users": [],
            "dm_sent_users": [],
            "used_tweets": [],
            "used_replies": []
        }
    
    def _save_state(self):
        """Save current bot state to file"""
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(self.state, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving state file: {e}")
    
    def _check_reset_daily_counters(self):
        """Reset daily counters if it's a new day"""
        today = datetime.now().strftime("%Y-%m-%d")
        if self.state["last_reset_date"] != today:
            logger.info("New day - resetting daily counters")
            self.state["last_reset_date"] = today
            self.state["tweets_posted_today"] = 0
            self.state["replies_sent_today"] = 0
            self.state["follows_today"] = 0
            self.state["dms_sent_today"] = 0
            self._save_state()
    
    def _load_content(self, filename):
        """Load content from file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f if line.strip()]
            else:
                logger.warning(f"Content file not found: {filename}")
                return []
        except Exception as e:
            logger.error(f"Error loading content file {filename}: {e}")
            return []
    
    def _get_next_tweet(self):
        """Get next tweet from rotation, avoiding repetition"""
        if not self.tweets:
            logger.warning("No tweets available")
            return None
        
        available_tweets = [t for t in self.tweets if t not in self.state["used_tweets"]]
        
        # If all tweets have been used, reset the used list
        if not available_tweets:
            logger.info("All tweets have been used, resetting rotation")
            self.state["used_tweets"] = []
            available_tweets = self.tweets
        
        tweet = random.choice(available_tweets)
        self.state["used_tweets"].append(tweet)
        return tweet
    
    def _get_next_reply(self):
        """Get next reply template from rotation"""
        if not self.replies:
            logger.warning("No replies available")
            return None
        
        available_replies = [r for r in self.replies if r not in self.state["used_replies"]]
        
        # If all replies have been used, reset the used list
        if not available_replies:
            logger.info("All replies have been used, resetting rotation")
            self.state["used_replies"] = []
            available_replies = self.replies
        
        reply = random.choice(available_replies)
        self.state["used_replies"].append(reply)
        return reply
    
    def _get_random_dm(self):
        """Get random DM template"""
        if not self.dms:
            logger.warning("No DM templates available")
            return None
        
        return random.choice(self.dms)
    
    def _update_rate_limit(self, endpoint, response=None):
        """Update rate limit information based on API response"""
        # If we have a response with rate limit headers, use those
        if response and hasattr(response, 'headers'):
            remaining = response.headers.get('x-rate-limit-remaining')
            reset_time = response.headers.get('x-rate-limit-reset')
            
            if remaining is not None and reset_time is not None:
                self.rate_limits[endpoint]["remaining"] = int(remaining)
                self.rate_limits[endpoint]["reset_time"] = int(reset_time)
                logger.debug(f"Updated rate limits for {endpoint}: {remaining} remaining, resets at {reset_time}")
                return
        
        # If we don't have headers, assume we used one request
        if endpoint in self.rate_limits:
            self.rate_limits[endpoint]["remaining"] = max(0, self.rate_limits[endpoint]["remaining"] - 1)
            logger.debug(f"Decremented rate limit for {endpoint}: {self.rate_limits[endpoint]['remaining']} remaining")
    
    def _check_rate_limit(self, endpoint):
        """Check if we're rate limited for a specific endpoint"""
        if endpoint not in self.rate_limits:
            return False
        
        # If we have remaining calls, we're not rate limited
        if self.rate_limits[endpoint]["remaining"] > 0:
            return False
        
        # Check if the reset time has passed
        current_time = time.time()
        if current_time >= self.rate_limits[endpoint]["reset_time"] + RATE_LIMIT_RESET_BUFFER:
            # Reset has passed, assume we have full quota again
            if endpoint == "search":
                self.rate_limits[endpoint]["remaining"] = 180
            elif endpoint == "tweet":
                self.rate_limits[endpoint]["remaining"] = 200
            elif endpoint == "follow":
                self.rate_limits[endpoint]["remaining"] = 50
            elif endpoint == "dm":
                self.rate_limits[endpoint]["remaining"] = 200
            
            self.rate_limits[endpoint]["reset_time"] = current_time + 900  # Default 15 min window
            return False
        
        # We're rate limited, calculate wait time
        wait_time = self.rate_limits[endpoint]["reset_time"] - current_time + RATE_LIMIT_RESET_BUFFER
        logger.info(f"Rate limited for {endpoint}. Need to wait {wait_time:.2f} seconds.")
        return wait_time
    
    def _api_request_with_backoff(self, endpoint, func, *args, **kwargs):
        """Make an API request with exponential backoff for rate limits"""
        retries = 0
        backoff = INITIAL_BACKOFF
        
        while retries <= MAX_RETRIES:
            # Check if we're rate limited
            wait_time = self._check_rate_limit(endpoint)
            if wait_time:
                wait_time = min(wait_time, MAX_BACKOFF)
                logger.info(f"Rate limited. Waiting {wait_time:.2f} seconds before retry.")
                time.sleep(wait_time)
            
            try:
                # Make the API request
                response = func(*args, **kwargs)
                
                # Update rate limit information
                self._update_rate_limit(endpoint, response)
                
                return response
            
            except tweepy.TooManyRequests as e:
                # Handle rate limit error
                logger.warning(f"Rate limit exceeded for {endpoint}: {e}")
                
                # Get reset time from error response if available
                reset_time = None
                if hasattr(e, 'response') and hasattr(e.response, 'headers'):
                    reset_time = e.response.headers.get('x-rate-limit-reset')
                
                if reset_time:
                    # Calculate wait time until reset
                    wait_time = int(reset_time) - time.time() + RATE_LIMIT_RESET_BUFFER
                    wait_time = max(0, min(wait_time, MAX_BACKOFF))
                    
                    # Update rate limit information
                    self.rate_limits[endpoint]["remaining"] = 0
                    self.rate_limits[endpoint]["reset_time"] = int(reset_time)
                else:
                    # Use exponential backoff
                    wait_time = backoff
                    backoff = min(backoff * 2, MAX_BACKOFF)
                
                logger.info(f"Waiting {wait_time:.2f} seconds before retry ({retries+1}/{MAX_RETRIES})")
                time.sleep(wait_time)
                retries += 1
            
            except Exception as e:
                logger.error(f"Error making API request to {endpoint}: {e}")
                
                # Use exponential backoff for other errors too
                wait_time = backoff
                backoff = min(backoff * 2, MAX_BACKOFF)
                
                logger.info(f"Waiting {wait_time:.2f} seconds before retry ({retries+1}/{MAX_RETRIES})")
                time.sleep(wait_time)
                retries += 1
        
        logger.error(f"Failed to make API request to {endpoint} after {MAX_RETRIES} retries")
        return None
    
    def should_post_tweet(self):
        """Check if it's time to post a new tweet"""
        # Check if we've reached the daily limit
        if self.state["tweets_posted_today"] >= 5:  # Max 5 tweets per day
            return False
        
        # Check if enough time has passed since last tweet
        last_tweet_time = self.state["last_tweet_time"]
        if last_tweet_time:
            last_tweet_dt = datetime.fromisoformat(last_tweet_time)
            hours_since_last_tweet = (datetime.now() - last_tweet_dt).total_seconds() / 3600
            return hours_since_last_tweet >= TWEET_INTERVAL_HOURS
        
        # No tweets posted yet today
        return True
    
    def should_find_and_reply(self):
        """Check if it's time to find tweets and reply"""
        # Check if we've reached the daily limit
        if self.state["replies_sent_today"] >= 24:  # Max 24 replies per day (1-2 per hour)
            return False
        
        # Check if enough time has passed since last reply
        last_reply_time = self.state["last_reply_time"]
        if last_reply_time:
            last_reply_dt = datetime.fromisoformat(last_reply_time)
            minutes_since_last_reply = (datetime.now() - last_reply_dt).total_seconds() / 60
            return minutes_since_last_reply >= REPLY_INTERVAL_MINUTES
        
        # No replies sent yet today
        return True
    
    def post_tweet(self):
        """Post a promotional tweet"""
        try:
            tweet_text = self._get_next_tweet()
            if not tweet_text:
                return False
            
            # Post tweet with backoff strategy
            response = self._api_request_with_backoff(
                "tweet",
                self.client_v2.create_tweet,
                text=tweet_text
            )
            
            if not response:
                logger.error("Failed to post tweet after retries")
                return False
            
            tweet_id = response.data['id']
            
            # Update state
            self.state["last_tweet_time"] = datetime.now().isoformat()
            self.state["tweets_posted_today"] += 1
            self._save_state()
            
            logger.info(f"Posted tweet: {tweet_text} (ID: {tweet_id})")
            return True
        
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False
    
    def find_and_reply_to_tweets(self):
        """Find relevant tweets and reply to them"""
        try:
            # Randomly select a hashtag to search
            hashtag = random.choice(TARGET_HASHTAGS)
            logger.info(f"Searching for tweets with hashtag: {hashtag}")
            
            # Search for recent tweets with the hashtag using backoff strategy
            query = f"{hashtag} -is:retweet -is:reply"
            tweets_response = self._api_request_with_backoff(
                "search",
                self.client_v2.search_recent_tweets,
                query=query,
                max_results=10,
                tweet_fields=['created_at', 'public_metrics']
            )
            
            if not tweets_response or not tweets_response.data:
                logger.info(f"No tweets found for hashtag: {hashtag}")
                return False
            
            # Filter tweets by engagement and check if we've already replied
            for tweet in tweets_response.data:
                tweet_id = tweet.id
                
                # Skip if we've already replied to this tweet
                if tweet_id in self.state["replied_to_tweets"]:
                    continue
                
                # Check if tweet has enough engagement
                likes = tweet.public_metrics['like_count']
                if likes < MIN_LIKES_THRESHOLD:
                    continue
                
                # Get reply text
                reply_text = self._get_next_reply()
                if not reply_text:
                    return False
                
                # Add a small delay before replying to avoid looking too bot-like
                time.sleep(random.uniform(5, 15))
                
                # Reply to tweet with backoff strategy
                response = self._api_request_with_backoff(
                    "tweet",
                    self.client_v2.create_tweet,
                    text=reply_text,
                    in_reply_to_tweet_id=tweet_id
                )
                
                if not response:
                    logger.error(f"Failed to reply to tweet {tweet_id} after retries")
                    return False
                
                # Update state
                self.state["last_reply_time"] = datetime.now().isoformat()
                self.state["replies_sent_today"] += 1
                self.state["replied_to_tweets"].append(tweet_id)
                self._save_state()
                
                logger.info(f"Replied to tweet {tweet_id} with: {reply_text}")
                return True
            
            logger.info("No suitable tweets found to reply to")
            return False
        
        except Exception as e:
            logger.error(f"Error finding and replying to tweets: {e}")
            return False
    
    def follow_users(self, enable_follows=False):
        """Find and follow users in target niche (optional)"""
        if not enable_follows:
            return False
        
        # Check if we've reached the daily limit
        if self.state["follows_today"] >= FOLLOW_LIMIT_PER_DAY:
            return False
        
        try:
            # Randomly select a hashtag to search
            hashtag = random.choice(TARGET_HASHTAGS)
            logger.info(f"Searching for users with hashtag: {hashtag}")
            
            # Search for recent tweets with the hashtag using backoff strategy
            query = f"{hashtag} -is:retweet -is:reply"
            tweets_response = self._api_request_with_backoff(
                "search",
                self.client_v2.search_recent_tweets,
                query=query,
                max_results=10,
                tweet_fields=['author_id']
            )
            
            if not tweets_response or not tweets_response.data:
                logger.info(f"No tweets found for hashtag: {hashtag}")
                return False
            
            # Find users to follow
            for tweet in tweets_response.data:
                user_id = tweet.author_id
                
                # Skip if we've already followed this user
                if user_id in self.state["followed_users"]:
                    continue
                
                # Add a small delay before following to avoid looking too bot-like
                time.sleep(random.uniform(5, 15))
                
                # Follow user with backoff strategy
                response = self._api_request_with_backoff(
                    "follow",
                    self.client_v2.follow_user,
                    user_id
                )
                
                if not response:
                    logger.error(f"Failed to follow user {user_id} after retries")
                    return False
                
                # Update state
                self.state["follows_today"] += 1
                self.state["followed_users"].append(user_id)
                self._save_state()
                
                logger.info(f"Followed user: {user_id}")
                return True
            
            logger.info("No suitable users found to follow")
            return False
        
        except Exception as e:
            logger.error(f"Error following users: {e}")
            return False
    
    def send_dms(self, enable_dms=False):
        """Send DMs to potential high-value users (optional)"""
        if not enable_dms:
            return False
        
        # Check if we've reached the daily limit
        if self.state["dms_sent_today"] >= DM_LIMIT_PER_DAY:
            return False
        
        try:
            # Get users we've followed but not DM'd yet
            potential_users = [
                user_id for user_id in self.state["followed_users"]
                if user_id not in self.state["dm_sent_users"]
            ]
            
            if not potential_users:
                logger.info("No potential users to DM")
                return False
            
            # Select a random user
            user_id = random.choice(potential_users)
            
            # Get DM text
            dm_text = self._get_random_dm()
            if not dm_text:
                return False
            
            # Add a small delay before sending DM to avoid looking too bot-like
            time.sleep(random.uniform(10, 30))
            
            # Send DM with backoff strategy (using v1 API)
            def send_dm_func():
                return self.client_v1.send_direct_message(user_id, dm_text)
            
            response = self._api_request_with_backoff("dm", send_dm_func)
            
            if not response:
                logger.error(f"Failed to send DM to user {user_id} after retries")
                return False
            
            # Update state
            self.state["dms_sent_today"] += 1
            self.state["dm_sent_users"].append(user_id)
            self._save_state()
            
            logger.info(f"Sent DM to user {user_id}: {dm_text}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending DMs: {e}")
            return False
    
    def run_once(self, enable_follows=False, enable_dms=False):
        """Run one iteration of the bot's main loop"""
        self._check_reset_daily_counters()
        
        # Check and post tweet if needed
        if self.should_post_tweet():
            self.post_tweet()
        
        # Check and reply to tweets if needed
        if self.should_find_and_reply():
            self.find_and_reply_to_tweets()
        
        # Optional: Follow users
        if enable_follows:
            self.follow_users(enable_follows)
        
        # Optional: Send DMs
        if enable_dms:
            self.send_dms(enable_dms)
    
    def run_forever(self, enable_follows=False, enable_dms=False, check_interval=60):
        """Run the bot continuously"""
        logger.info("Starting LushMeet Twitter Bot...")
        
        try:
            while True:
                self.run_once(enable_follows, enable_dms)
                
                # Add jitter to check interval to avoid predictable patterns
                jitter = random.uniform(0.8, 1.2)
                sleep_time = check_interval * jitter
                logger.debug(f"Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise


if __name__ == "__main__":
    # Check if required environment variables are set
    missing_vars = []
    for var in ["TWITTER_API_KEY", "TWITTER_API_SECRET", "TWITTER_ACCESS_TOKEN", 
                "TWITTER_ACCESS_SECRET", "TWITTER_BEARER_TOKEN"]:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in a .env file or environment")
        exit(1)
    
    # Check if content files exist
    for file in ["tweets.txt", "replies.txt"]:
        if not os.path.exists(file):
            logger.error(f"Required content file {file} not found")
            exit(1)
    
    # Create and run the bot
    bot = LushMeetTwitterBot()
    
    # Uncomment to enable optional features
    # ENABLE_FOLLOWS = True  # Set to True to enable following users
    # ENABLE_DMS = True      # Set to True to enable sending DMs
    
    # Run the bot (default: follows and DMs disabled)
    bot.run_forever(enable_follows=False, enable_dms=False, check_interval=120)  # Check every 2 minutes by default
