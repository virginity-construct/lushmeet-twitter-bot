# LushMeet Twitter Bot: Authentication Guide

## Required Authentication for LushMeet Bot Features

Based on the Twitter API documentation, here's what we need for each feature:

| Feature | Authentication Required | Status |
|---------|------------------------|--------|
| Post scheduled tweets | OAuth 1.0a User Context | ⚠️ Need Access Token & Secret |
| Reply to trending tweets | OAuth 1.0a User Context | ⚠️ Need Access Token & Secret |
| Follow users (optional) | OAuth 1.0a User Context | ⚠️ Need Access Token & Secret |
| Send DMs (optional) | OAuth 1.0a User Context | ⚠️ Need Access Token & Secret |

## Step-by-Step Guide to Generate Access Token & Secret

1. **Log in to Twitter Developer Portal**
   - Go to [developer.twitter.com](https://developer.twitter.com)
   - Sign in with the @LushMeet account

2. **Navigate to Your Project**
   - Go to "Projects & Apps" in the dashboard
   - Select your project (or create one if needed)
   - Select your app (or create one if needed)

3. **Enable OAuth 1.0a**
   - In your app settings, navigate to the "Authentication settings" tab
   - Enable OAuth 1.0a
   - Set App permissions to "Read and Write"
   - Set Type of App to "Web App, Automated App or Bot"
   - Add a Callback URL (can be http://localhost if you don't have a specific one)
   - Add a Website URL (your LushMeet website or a placeholder)
   - Save changes

4. **Generate Access Token & Secret**
   - In the "Keys and tokens" tab
   - Scroll to "Authentication Tokens" section
   - Click "Generate" under "Access Token and Secret"
   - This will create tokens with the permissions you set earlier
   - **Important**: Save these tokens immediately as they won't be shown again

5. **Update Your .env File**
   ```
   TWITTER_API_KEY=SGNIQ2FiU0I4Y0Y2NHFmMFRFYVg6MTpjaQ
   TWITTER_API_SECRET=fLges4JbZDV_pkWIG67Sl45g5BPWOBR_2GO6HsKCg5BwrP9Wbv
   TWITTER_ACCESS_TOKEN=your_new_access_token
   TWITTER_ACCESS_SECRET=your_new_access_secret
   TWITTER_BEARER_TOKEN=your_bearer_token
   ```

6. **Verify Authentication**
   - Run `python test_connection.py` to verify connection
   - Run `python test_tweet.py` to verify posting ability

## Troubleshooting

If you encounter authentication errors:

1. **Check Permissions**: Ensure your app has "Read and Write" permissions
2. **Token Expiration**: OAuth 2.0 tokens can expire; OAuth 1.0a tokens generally don't
3. **Rate Limits**: Twitter has strict rate limits; the bot has built-in protections
4. **App Status**: Ensure your Twitter Developer account is in good standing

## Maintaining LushMeet's Luxury Aesthetic

Remember that all bot interactions should maintain LushMeet's "Private. Unapologetic. Untouchable." brand voice. The authentication setup ensures the bot can properly represent your exclusive platform with the appropriate tone and engagement strategy.
