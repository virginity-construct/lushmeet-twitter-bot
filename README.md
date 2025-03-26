# LushMeet Twitter Bot — Dev Handoff

**Project Path:**  
`C:\Users\pjv43\CascadeProjects\lushmeet-twitter-bot\`

**Goal:**  
Automated brand presence for [@LushMeet](https://x.com/LushMeet) with luxury tone, consistent output, and subtle engagement.

## Features

- **Scheduled Tweets**: Posts promotional content at regular intervals (4-6 hours)
- **Trending Replies**: Finds and replies to relevant tweets in the target niche
- **Optional Follow/DM**: Can follow users and send personalized DMs (disabled by default)
- **Rate Limiting**: Built-in protections against Twitter API rate limits
- **State Tracking**: Remembers which tweets have been replied to and tracks daily limits

## Setup

### Prerequisites

- Python 3.7+
- Twitter Developer Account with Elevated API access
- Twitter API v2 credentials

### Installation

1. Clone this repository or download the files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Twitter API credentials:
   - Copy `.env.example` to `.env`
   - Fill in your Twitter API credentials in the `.env` file

### Configuration

The bot can be configured by editing the variables at the top of `main.py`:

- `TWEET_INTERVAL_HOURS`: Hours between tweets (default: random 4-6)
- `REPLY_INTERVAL_MINUTES`: Minutes between replies (default: random 30-60)
- `FOLLOW_LIMIT_PER_DAY`: Maximum accounts to follow per day (default: 10)
- `DM_LIMIT_PER_DAY`: Maximum DMs to send per day (default: 5)
- `MIN_LIKES_THRESHOLD`: Minimum likes for a tweet to be considered for reply (default: 10)
- `TARGET_HASHTAGS`: List of hashtags to search for tweets to reply to

### Content Customization

The bot uses three text files for content:

- `tweets.txt`: One tweet per line, used for scheduled tweets
- `replies.txt`: One reply template per line, used for replying to tweets
- `dms.txt`: One DM template per line, used for sending direct messages

Edit these files to customize the content according to your brand voice.

## Usage

### Running Locally

To run the bot locally:

```bash
python main.py
```

The bot will run continuously, checking for opportunities to tweet or reply based on the configured intervals.

### Deployment Options

#### Replit

1. Create a new Replit project and upload all files
2. Add your Twitter API credentials as Secrets in Replit
3. Install dependencies in the Replit Shell:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.replit` file with:
   ```
   run = "python main.py"
   ```
5. Use Replit's "Always On" feature to keep the bot running

#### GitHub Actions

1. Create a new GitHub repository and push all files
2. Add your Twitter API credentials as GitHub Secrets
3. Create a workflow file at `.github/workflows/bot.yml`:

```yaml
name: Run Twitter Bot

on:
  schedule:
    - cron: '*/15 * * * *'  # Run every 15 minutes
  workflow_dispatch:  # Allow manual trigger

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run bot
        env:
          TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
          TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
          TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          TWITTER_ACCESS_SECRET: ${{ secrets.TWITTER_ACCESS_SECRET }}
          TWITTER_BEARER_TOKEN: ${{ secrets.TWITTER_BEARER_TOKEN }}
        run: python github_action_runner.py
```

4. Create a `github_action_runner.py` file:

```python
#!/usr/bin/env python3
from main import LushMeetTwitterBot

# Create and run the bot once (for GitHub Actions)
bot = LushMeetTwitterBot()
bot.run_once(enable_follows=False, enable_dms=False)
```

## Advanced Features

### Enabling Follows and DMs

By default, the follow and DM features are disabled. To enable them:

1. Open `main.py`
2. Find the section at the bottom with the commented lines:
   ```python
   # Uncomment to enable optional features
   # ENABLE_FOLLOWS = True  # Set to True to enable following users
   # ENABLE_DMS = True      # Set to True to enable sending DMs
   ```
3. Uncomment these lines and set them to `True` as desired
4. Update the `bot.run_forever()` call with your chosen parameters

### Logging

The bot logs all activities to both the console and a `bot.log` file. Check this file for debugging information if you encounter any issues.

## Twitter API Rate Limits

Twitter API has rate limits that restrict how many requests you can make in a time period. The bot is designed to work within these limits, but be aware of the following:

- Tweet posting: 200 tweets per 3 hours
- Tweet replies: 300 per 3 hours
- Following users: 400 per day
- Direct messages: 1000 per day

The bot's default settings are well below these limits to ensure safe operation.

## Legal and Ethical Considerations

- Ensure your bot complies with Twitter's Terms of Service and Developer Agreement
- Be respectful in your automated interactions
- Do not spam or harass users
- Clearly identify automated content when required by platform policies

## Troubleshooting

- **API Errors**: Check your API credentials and ensure they have the correct permissions
- **Content Issues**: Ensure your content files exist and contain valid content
- **Rate Limiting**: If you encounter rate limit errors, reduce the frequency of actions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Stack Overview
- **Language:** Python 3.x  
- **Core Library:** Tweepy  
- **Environment:** dotenv-based config  
- **Deployment Options:**  
  - Local (`run_bot.bat`)
  - Replit (free hosting, always-on)
  - GitHub Actions (scheduled via cron)

## Bonus: AI Integration (Optional)
You can plug in your **OpenAI API key** for GPT-enhanced replies or tweet generation:
- Add `OPENAI_API_KEY` to `.env`
- Use `openai.ChatCompletion` in the reply handler
- Prompt suggestions preloaded in `gpt_prompts.txt` (coming soon)

## Brand Voice
- **Tagline:** "Private. Unapologetic. Untouchable."  
- **Vibe:** Luxury, exclusive, minimal, confident  
- **Reply Strategy:** Understated, seductive, never thirsty

## Next Steps
- Push to GitHub (private) or deploy via Replit  
- Monitor engagement and refine reply triggers weekly
- Consider GPT-powered generation or analytics dashboard next
