# Configuration settings for the Telegram bot
import os

# Get bot token from environment variables
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# Messages
WELCOME_MESSAGE = """
Welcome to Twitter/X Video Downloader Bot! 🎥
Send me a Twitter/X video URL, and I'll download and send it back to you.
Use /help for more information.
"""

HELP_MESSAGE = """
📖 *How to use this bot:*

1. Find a Twitter/X video you want to download
2. Copy the video's URL
3. Send the URL to this bot
4. Wait for the bot to process and send your video

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
