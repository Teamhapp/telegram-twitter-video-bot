# Configuration settings for the Telegram bot
import os

# Get bot token from environment variables
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# Messages
WELCOME_MESSAGE = """
Welcome to Twitter/X Video Downloader Bot! 🎥
Send me a Twitter/X video URL or thread URL, and I'll download and send the videos to you.
Use /help for more information.
"""

HELP_MESSAGE = """
📖 *How to use this bot:*

1. Find a Twitter/X video or thread you want to download
2. Copy the video's URL or thread URL
3. Send the URL to this bot
4. Wait for the bot to process and send your video(s)

*Supported URLs:*
• Single video URLs
• Thread URLs (downloads all videos in the thread)

*Supported Commands:*
/start - Start the bot
/help - Show this help message

*Note:* Only Twitter/X video URLs are supported.
"""

# Temporary directory for downloaded videos
TEMP_DIR = "temp"

# Valid URL patterns
TWITTER_URL_PATTERNS = [
    "twitter.com",
    "x.com"
]
