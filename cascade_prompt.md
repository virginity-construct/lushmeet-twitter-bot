# LushMeet Twitter Bot Generator Prompt

## Task Description
Create a complete Twitter bot for LushMeet, a private, invite-only matching platform connecting verified clients with high-end companions. The bot should promote LushMeet on Twitter through scheduled tweets, replies to trending niche tweets, and optional follow/DM functionality. The implementation must use a 100% free stack.

## Technical Requirements
- Python 3.x with Tweepy library for Twitter API v2 integration
- Flat file storage (.txt or .json) for tweet content and state management
- Deployment options for Replit, GitHub Actions (with cron jobs), or local execution
- Environment variables for secure credential storage
- Comprehensive error handling and rate limit management
- Logging system for tracking bot activities

## Bot Features

### 1. Scheduled Tweets
- Pull promotional content from a predefined list in `tweets.txt` or JSON array
- Post tweets at regular intervals (every 4-6 hours)
- Track posted tweets to avoid repetition
- Include luxury-themed hashtags and CTAs

### 2. Reply to Trending Tweets
- Search for tweets containing relevant hashtags: `#sugarbaby`, `#escortlife`, `#onlyfans`, `#luxury`, `GFE`
- Filter tweets based on engagement metrics (likes > 10, recent)
- Reply with subtle, on-brand CTAs that drive curiosity
- Implement rate limiting to avoid Twitter API restrictions

### 3. Optional: Strategic Follows and DMs
- Identify and follow active users in the target niche
- Send personalized, subtle DMs to potential high-value users
- Track sent DMs to avoid duplicate messages
- Implement proper timing delays between actions

## Required Files
1. `main.py`: Core bot logic and execution flow
2. `tweets.txt`: Collection of branded tweets for rotation
3. `replies.txt`: Template responses for trending tweet replies
4. `.env.example`: Template for environment variables (API keys)
5. `requirements.txt`: Dependencies (tweepy, python-dotenv, etc.)
6. `README.md`: Comprehensive setup, configuration, and deployment guide
7. Optional deployment files for Replit or GitHub Actions

## Brand Voice Guidelines
- Luxury-focused: Emphasize exclusivity, high-end experience
- Subtle yet assertive: Not overly promotional but confident
- Professional: No explicit content, focus on connections and quality
- Exclusive: Emphasize the invite-only, vetted nature of the platform

## Example Content

### Tweet Examples
```
"Private. Pre-screened. Profitable. LushMeet is where elite meets elite. DM for access. 💎"
"All your fav sugarbabies are already on LushMeet 👀"
"$5K bookings, no timewasters. You ready to play or still tweeting for likes?"
"Private network. No ads. No simps. Just money. DM for access."
"Escort ads dying? LushMeet is built different. Apply quietly."
"Luxury meets privacy. LushMeet is live. DM for access 💎"
"No middlemen. No ads. Just elite bookings. You ready?"
```

### Reply Examples
```
"Sounds like someone belongs on LushMeet 💎 (invite-only, DM if curious)"
"Looks like you'd belong on LushMeet. Invite-only 💎"
"We're building something you might appreciate. High-end, no drama. DM if interested."
```

### DM Examples
```
"Saw your profile. I run LushMeet, a high-end invite-only platform. Might be worth chatting."
"Building something you might vibe with. High-end, no drama. DM if open to invites."
```

## Implementation Details
- Ensure proper error handling for Twitter API rate limits
- Implement random timing between actions to appear more human-like
- Store state information to track which tweets have been replied to
- Include logging for debugging and performance tracking
- Design the code to be easily extensible for future features

Please generate all the required files for a complete, production-ready Twitter bot implementation based on these specifications.
