# LushMeet Twitter API Setup Guide

## Overview

This guide will help you properly set up Twitter API credentials for the LushMeet Twitter bot, ensuring it maintains your luxury branding and exclusive tone.

## Step 1: Create a Twitter Developer Account

1. Sign in to [Twitter Developer Portal](https://developer.twitter.com) with your @LushMeet account
2. Apply for Elevated access (required for posting tweets)
3. Create a new Project (name it "LushMeet Engagement")
4. Create a new App within that project (name it "LushMeet Bot")

## Step 2: Configure App Permissions

1. In your App settings, navigate to "User authentication settings"
2. Enable OAuth 1.0a
3. Set App permissions to "Read and Write"
4. Set Type of App to "Web App, Automated App or Bot"
5. Add a Callback URL (can be http://localhost)
6. Add a Website URL (your LushMeet website)
7. Save changes

## Step 3: Generate New API Keys and Tokens

Twitter has different types of authentication:
- **OAuth 2.0** (for read-only operations)
- **OAuth 1.0a** (required for posting tweets)

### Generate OAuth 2.0 Credentials
1. In "Keys and tokens" tab, find "OAuth 2.0 Client ID and Client Secret"
2. Click "Regenerate" if needed

### Generate OAuth 1.0a Credentials
1. In "Keys and tokens" tab, find "API Key and Secret"
2. Click "Regenerate" if needed
3. Find "Access Token and Secret" 
4. Click "Generate" (these must be generated with Read+Write permissions)

## Step 4: Update Your .env File

```
# Consumer Keys (OAuth 1.0a)
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret

# Authentication Tokens (OAuth 1.0a)
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

# Bearer Token (OAuth 2.0)
TWITTER_BEARER_TOKEN=your_bearer_token
```

## Common Issues

1. **Mixing OAuth 2.0 and OAuth 1.0a credentials**: Make sure you're using the API Key and Secret from the OAuth 1.0a section, not the OAuth 2.0 Client ID and Secret.

2. **Insufficient permissions**: Ensure your app has "Read and Write" permissions and that your Access Token was generated after setting these permissions.

3. **Token format**: 
   - Access Token should be in format: `1234567890-abcdefghijklmnopqrstuvwxyz`
   - Bearer Token should start with `AAAA`

4. **App approval**: If you recently created your app, there might be a delay before it's fully activated.

## Testing Your Setup

After updating your credentials, run:
```
python test_v2_tweet.py
```

This will verify if your bot can authenticate and post tweets.

## Maintaining LushMeet's Luxury Aesthetic

Once properly configured, your Twitter bot will maintain LushMeet's "Private. Unapologetic. Untouchable." brand voice, posting exclusive content and engaging with potential clients in a way that emphasizes the invitation-only nature of your platform.

The dark theme with gold highlights aesthetic of your platform will be reflected in the sophisticated, authoritative tone of your Twitter presence, reinforcing your luxury branding across all touchpoints.
