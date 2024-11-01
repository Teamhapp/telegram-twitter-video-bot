# Configuration settings for the Telegram bot
import os

# Get bot token from environment variables
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# Video quality options
VIDEO_QUALITIES = {
    'best': 'Best available quality',
    'medium': 'Medium quality (480p if available)',
    'low': 'Low quality (240p if available)'
}

# Default quality
DEFAULT_QUALITY = 'best'

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

*Video Quality Options:*
Use these commands to set your preferred video quality:
/quality_best - Best available quality (default)
/quality_medium - Medium quality (480p if available)
/quality_low - Low quality (240p if available)

*Supported URLs:*
• Single video URLs
• Thread URLs (downloads all videos in the thread)

*Supported Commands:*
/start - Start the bot
/help - Show this help message
/quality - Show current quality setting

*Note:* Only Twitter/X video URLs are supported.
"""

# Temporary directory for downloaded videos
TEMP_DIR = "temp"

# Valid URL patterns
TWITTER_URL_PATTERNS = [
    "twitter.com",
    "x.com"
]
