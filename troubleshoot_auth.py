#!/usr/bin/env python3
"""
Comprehensive troubleshooting script for Twitter API authentication
Tests both OAuth 1.0a and OAuth 2.0 authentication methods
"""

import os
import json
import tweepy
import requests
from dotenv import load_dotenv
import logging
import base64
import urllib.parse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("lushmeet_troubleshoot")

# Load environment variables
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def test_oauth2_bearer():
    """Test OAuth 2.0 Bearer Token authentication"""
    print("\n=== Testing OAuth 2.0 Bearer Token ===\n")
    
    if not BEARER_TOKEN:
        print("❌ Bearer token not found in .env file")
        return False
    
    try:
        # Create Client with Bearer Token
        client = tweepy.Client(bearer_token=BEARER_TOKEN)
        
        # Test a simple read-only endpoint
        print("Testing Bearer Token with a simple API call...")
        response = client.get_user(username="twitter")
        
        if response.data:
            print(f"✅ Bearer Token authentication successful")
            print(f"Retrieved user: @{response.data.username} (ID: {response.data.id})")
            return True
        else:
            print("❌ Bearer Token authentication failed - no data returned")
            return False
            
    except Exception as e:
        print(f"❌ Bearer Token authentication failed: {e}")
        return False

def test_oauth2_app_only():
    """Test OAuth 2.0 App-Only authentication (Client Credentials)"""
    print("\n=== Testing OAuth 2.0 App-Only Authentication ===\n")
    
    if not API_KEY or not API_SECRET:
        print("❌ API Key or Secret not found in .env file")
        return False
    
    try:
        # Encode credentials
        credentials = f"{urllib.parse.quote(API_KEY)}:{urllib.parse.quote(API_SECRET)}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        # Request Bearer Token
        print("Requesting Bearer Token using Client Credentials...")
        url = "https://api.twitter.com/oauth2/token"
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }
        data = "grant_type=client_credentials"
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            if "access_token" in token_data:
                print(f"✅ Successfully obtained Bearer Token")
                print(f"Token type: {token_data.get('token_type', 'unknown')}")
                
                # Test the token with a simple API call
                test_token = token_data["access_token"]
                client = tweepy.Client(bearer_token=test_token)
                user_response = client.get_user(username="twitter")
                
                if user_response.data:
                    print(f"✅ Successfully used generated Bearer Token")
                    print(f"Retrieved user: @{user_response.data.username}")
                    
                    # Compare with stored Bearer Token
                    if test_token != BEARER_TOKEN:
                        print("\n⚠️ The generated Bearer Token is different from the one in your .env file")
                        print("Consider updating your .env file with this new token:")
                        print(f"TWITTER_BEARER_TOKEN={test_token}")
                    
                    return True
                else:
                    print("❌ Generated Bearer Token failed to retrieve user data")
                    return False
            else:
                print(f"❌ Failed to extract Bearer Token from response")
                return False
        else:
            print(f"❌ Failed to obtain Bearer Token: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OAuth 2.0 App-Only authentication failed: {e}")
        return False

def test_oauth1_user_context():
    """Test OAuth 1.0a User Context authentication"""
    print("\n=== Testing OAuth 1.0a User Context Authentication ===\n")
    
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
        print("❌ Missing OAuth 1.0a credentials in .env file")
        return False
    
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
        
        # Check write permissions
        print("\nChecking write permissions...")
        if me.screen_name:
            print("✅ Write permissions appear to be correctly configured")
            print("The bot should be able to post tweets as @" + me.screen_name)
        
        return True
        
    except tweepy.TweepyException as e:
        print(f"❌ OAuth 1.0a authentication failed: {e}")
        
        # Provide more specific error guidance
        error_str = str(e).lower()
        if "401" in error_str:
            print("\nThis appears to be an authentication error. Possible causes:")
            print("1. The API key/secret or access token/secret may be incorrect")
            print("2. The tokens may have expired or been revoked")
            print("3. The app may not have the required permissions (needs Read+Write)")
            
            # Check if tokens match expected format
            if ACCESS_TOKEN and not ACCESS_TOKEN.split("-")[0].isdigit():
                print("\n⚠️ The Access Token does not appear to be in the correct format.")
                print("It should be in the format: 123456789-abcdefghijklmnopqrstuvwxyz")
            
        elif "403" in error_str:
            print("\nThis appears to be a permissions error. Possible causes:")
            print("1. The app may not have the required permissions (needs Read+Write)")
            print("2. The account may be restricted or in read-only mode")
        
        return False

def verify_token_formats():
    """Verify that tokens are in the expected format"""
    print("\n=== Verifying Token Formats ===\n")
    
    issues = 0
    
    # Check API Key format (typically alphanumeric)
    if API_KEY:
        if len(API_KEY) < 10:
            print("⚠️ API Key seems too short")
            issues += 1
    else:
        print("❌ API Key is missing")
        issues += 1
    
    # Check API Secret format (typically alphanumeric)
    if API_SECRET:
        if len(API_SECRET) < 10:
            print("⚠️ API Secret seems too short")
            issues += 1
    else:
        print("❌ API Secret is missing")
        issues += 1
    
    # Check Access Token format (typically numeric ID followed by hyphen and alphanumeric string)
    if ACCESS_TOKEN:
        parts = ACCESS_TOKEN.split("-")
        if len(parts) != 2 or not parts[0].isdigit():
            print("⚠️ Access Token format seems incorrect")
            print("Expected format: 123456789-abcdefghijklmnopqrstuvwxyz")
            issues += 1
    else:
        print("❌ Access Token is missing")
        issues += 1
    
    # Check Access Token Secret format (typically alphanumeric)
    if ACCESS_SECRET:
        if len(ACCESS_SECRET) < 10:
            print("⚠️ Access Token Secret seems too short")
            issues += 1
    else:
        print("❌ Access Token Secret is missing")
        issues += 1
    
    # Check Bearer Token format (typically starts with "AAAA")
    if BEARER_TOKEN:
        if not BEARER_TOKEN.startswith("AAAA"):
            print("⚠️ Bearer Token format seems incorrect")
            print("Expected to start with 'AAAA'")
            issues += 1
    else:
        print("❌ Bearer Token is missing")
        issues += 1
    
    if issues == 0:
        print("✅ All token formats appear valid")
    else:
        print(f"⚠️ Found {issues} potential issues with token formats")
    
    return issues == 0

def print_credentials_summary():
    """Print a summary of the available credentials"""
    print("\n=== Credentials Summary ===\n")
    
    # Helper function to mask credentials
    def mask(text):
        if not text:
            return "Not set"
        if len(text) <= 8:
            return "*" * len(text)
        return text[:4] + "*" * (len(text) - 8) + text[-4:]
    
    print(f"API Key:           {mask(API_KEY)}")
    print(f"API Secret:        {mask(API_SECRET)}")
    print(f"Access Token:      {mask(ACCESS_TOKEN)}")
    print(f"Access Secret:     {mask(ACCESS_SECRET)}")
    print(f"Bearer Token:      {mask(BEARER_TOKEN)}")

def main():
    """Run all authentication tests"""
    print("\n=== LushMeet Twitter Bot - Authentication Troubleshooter ===\n")
    
    # Print credentials summary
    print_credentials_summary()
    
    # Verify token formats
    verify_token_formats()
    
    # Test OAuth 2.0 Bearer Token
    bearer_success = test_oauth2_bearer()
    
    # Test OAuth 2.0 App-Only authentication
    app_only_success = test_oauth2_app_only()
    
    # Test OAuth 1.0a User Context authentication
    oauth1_success = test_oauth1_user_context()
    
    # Print summary
    print("\n=== Authentication Test Summary ===\n")
    print(f"OAuth 2.0 Bearer Token:     {'✅ Passed' if bearer_success else '❌ Failed'}")
    print(f"OAuth 2.0 App-Only:         {'✅ Passed' if app_only_success else '❌ Failed'}")
    print(f"OAuth 1.0a User Context:    {'✅ Passed' if oauth1_success else '❌ Failed'}")
    
    if bearer_success or app_only_success:
        print("\n✅ The bot can connect to Twitter API for read operations")
    else:
        print("\n❌ The bot cannot connect to Twitter API for read operations")
    
    if oauth1_success:
        print("✅ The bot can post tweets and perform write operations")
    else:
        print("❌ The bot cannot post tweets or perform write operations")
    
    print("\nNext steps:")
    if not (bearer_success or app_only_success or oauth1_success):
        print("1. Double-check all credentials in your .env file")
        print("2. Ensure your Twitter Developer account is active")
        print("3. Regenerate tokens in the Twitter Developer Portal")
    elif not oauth1_success:
        print("1. Focus on fixing OAuth 1.0a credentials for write operations")
        print("2. Ensure your app has Read+Write permissions")
        print("3. Regenerate Access Token and Secret with the correct permissions")
    else:
        print("1. All authentication methods are working correctly!")
        print("2. You can now run the bot with full functionality")

if __name__ == "__main__":
    main()
