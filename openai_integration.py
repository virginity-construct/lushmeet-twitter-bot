#!/usr/bin/env python3
"""
OpenAI Integration for LushMeet Twitter Bot
Enhances the bot with AI-powered content generation
"""

import os
import json
import logging
import openai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("openai.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("lushmeet_openai")

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class LushMeetAI:
    """AI content generation for LushMeet Twitter Bot"""
    
    def __init__(self):
        """Initialize the AI with OpenAI API key"""
        if not OPENAI_API_KEY:
            logger.warning("OpenAI API key not found. AI features will be disabled.")
            self.enabled = False
        else:
            openai.api_key = OPENAI_API_KEY
            self.enabled = True
            self.prompts = self._load_prompts()
            logger.info("LushMeet AI initialized")
    
    def _load_prompts(self):
        """Load GPT prompts from file"""
        prompts = {}
        try:
            with open("gpt_prompts.txt", 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Parse sections
                sections = content.split('## ')
                for section in sections:
                    if not section.strip():
                        continue
                    
                    lines = section.strip().split('\n')
                    if lines:
                        key = lines[0].lower().replace(' ', '_').replace('prompt', '')
                        value = '\n'.join(lines[1:]).strip()
                        prompts[key] = value
            
            return prompts
        
        except Exception as e:
            logger.error(f"Error loading prompts: {e}")
            # Fallback prompts
            return {
                "tweet_generation": "Generate a luxury-focused tweet for LushMeet, a private platform connecting clients with companions. Use subtle language that implies exclusivity. Keep it under 280 characters.",
                "reply_generation": "Create a subtle, luxury-focused reply that positions LushMeet as the premium alternative. Keep it under 200 characters.",
                "dm_generation": "Write a personalized, subtle direct message introducing LushMeet as an exclusive platform. Keep it under 300 characters."
            }
    
    def generate_tweet(self):
        """Generate a luxury-focused tweet using GPT"""
        if not self.enabled:
            return None
        
        try:
            prompt = self.prompts.get("tweet_generation", "Generate a luxury tweet for LushMeet")
            
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use gpt-3.5-turbo for lower cost
                messages=[
                    {"role": "system", "content": "You are a luxury brand copywriter for an exclusive high-end service."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            tweet = response.choices[0].message.content.strip()
            
            # Remove quotes if present
            if tweet.startswith('"') and tweet.endswith('"'):
                tweet = tweet[1:-1]
            
            logger.info(f"Generated tweet: {tweet}")
            return tweet
        
        except Exception as e:
            logger.error(f"Error generating tweet: {e}")
            return None
    
    def generate_reply(self, topic):
        """Generate a reply to a tweet based on its topic"""
        if not self.enabled:
            return None
        
        try:
            prompt_template = self.prompts.get("reply_generation", "Create a luxury reply about {topic}")
            prompt = prompt_template.replace("{topic}", topic)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use gpt-3.5-turbo for lower cost
                messages=[
                    {"role": "system", "content": "You are a luxury brand representative responding to social media posts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=80,
                temperature=0.7
            )
            
            reply = response.choices[0].message.content.strip()
            
            # Remove quotes if present
            if reply.startswith('"') and reply.endswith('"'):
                reply = reply[1:-1]
            
            logger.info(f"Generated reply for topic '{topic}': {reply}")
            return reply
        
        except Exception as e:
            logger.error(f"Error generating reply: {e}")
            return None
    
    def generate_dm(self, niche):
        """Generate a personalized DM based on user's niche"""
        if not self.enabled:
            return None
        
        try:
            prompt_template = self.prompts.get("dm_generation", "Write a personalized message about {niche}")
            prompt = prompt_template.replace("{niche}", niche)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use gpt-3.5-turbo for lower cost
                messages=[
                    {"role": "system", "content": "You are a luxury brand representative reaching out to potential high-value clients."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=120,
                temperature=0.7
            )
            
            dm = response.choices[0].message.content.strip()
            
            # Remove quotes if present
            if dm.startswith('"') and dm.endswith('"'):
                dm = dm[1:-1]
            
            logger.info(f"Generated DM for niche '{niche}': {dm}")
            return dm
        
        except Exception as e:
            logger.error(f"Error generating DM: {e}")
            return None
    
    def refine_content(self, original_content):
        """Refine content to better match LushMeet's luxury branding"""
        if not self.enabled:
            return original_content
        
        try:
            prompt_template = self.prompts.get("content_refinement", "Refine this content: {original_content}")
            prompt = prompt_template.replace("{original_content}", original_content)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use gpt-3.5-turbo for lower cost
                messages=[
                    {"role": "system", "content": "You are a luxury brand copywriter refining social media content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5
            )
            
            refined = response.choices[0].message.content.strip()
            
            # Remove quotes if present
            if refined.startswith('"') and refined.endswith('"'):
                refined = refined[1:-1]
            
            logger.info(f"Refined content: {refined}")
            return refined
        
        except Exception as e:
            logger.error(f"Error refining content: {e}")
            return original_content
    
    def suggest_hashtags(self):
        """Suggest relevant luxury-focused hashtags"""
        if not self.enabled:
            return []
        
        try:
            prompt = self.prompts.get("hashtag_suggestion", "Suggest 3-5 luxury hashtags for LushMeet")
            
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use gpt-3.5-turbo for lower cost
                messages=[
                    {"role": "system", "content": "You are a social media strategist for a luxury brand."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.7
            )
            
            hashtags_text = response.choices[0].message.content.strip()
            
            # Extract hashtags
            hashtags = []
            for word in hashtags_text.split():
                if word.startswith('#'):
                    hashtags.append(word)
            
            logger.info(f"Suggested hashtags: {hashtags}")
            return hashtags
        
        except Exception as e:
            logger.error(f"Error suggesting hashtags: {e}")
            return []
    
    def analyze_engagement(self, conversation):
        """Analyze a Twitter conversation to determine if user is a good fit"""
        if not self.enabled:
            return None
        
        try:
            prompt_template = self.prompts.get("engagement_analysis", "Analyze this conversation: {conversation}")
            prompt = prompt_template.replace("{conversation}", conversation)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use gpt-3.5-turbo for lower cost
                messages=[
                    {"role": "system", "content": "You are a luxury brand representative analyzing social media conversations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            analysis = response.choices[0].message.content.strip()
            logger.info(f"Engagement analysis completed")
            return analysis
        
        except Exception as e:
            logger.error(f"Error analyzing engagement: {e}")
            return None


if __name__ == "__main__":
    # Test the AI functionality
    ai = LushMeetAI()
    
    if ai.enabled:
        print("\n=== LushMeet AI Test ===\n")
        
        print("Generating tweet...")
        tweet = ai.generate_tweet()
        print(f"Tweet: {tweet}\n")
        
        print("Generating reply...")
        reply = ai.generate_reply("luxury lifestyle")
        print(f"Reply: {reply}\n")
        
        print("Generating DM...")
        dm = ai.generate_dm("high-end modeling")
        print(f"DM: {dm}\n")
        
        print("Suggesting hashtags...")
        hashtags = ai.suggest_hashtags()
        print(f"Hashtags: {' '.join(hashtags)}\n")
        
        print("Refining content...")
        original = "Join LushMeet for exclusive connections."
        refined = ai.refine_content(original)
        print(f"Original: {original}")
        print(f"Refined: {refined}\n")
    else:
        print("OpenAI integration is disabled. Set OPENAI_API_KEY in .env file to enable.")
