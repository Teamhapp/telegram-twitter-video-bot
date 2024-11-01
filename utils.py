import os
import re
import uuid
from urllib.parse import urlparse
from config import TWITTER_URL_PATTERNS, TEMP_DIR
from telegram import Bot, Update, ChatMember
from telegram.error import TelegramError

def is_valid_twitter_url(url: str) -> bool:
    """
    Validate if the provided URL is a valid Twitter/X URL
    """
    try:
        parsed = urlparse(url)
        return any(pattern in parsed.netloc for pattern in TWITTER_URL_PATTERNS)
    except:
        return False

def is_thread_url(url: str) -> bool:
    """
    Check if the URL is a Twitter/X thread URL
    """
    try:
        parsed = urlparse(url)
        path_parts = parsed.path.split('/')
        return 'status' in path_parts and len(path_parts) > 3
    except:
        return False

def generate_temp_filename() -> str:
    """
    Generate a unique temporary filename
    """
    return os.path.join(TEMP_DIR, f"{uuid.uuid4()}.mp4")

def cleanup_temp_file(filepath: str) -> None:
    """
    Remove temporary downloaded file
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Error cleaning up file {filepath}: {str(e)}")

def ensure_temp_dir_exists():
    """
    Ensure temporary directory exists
    """
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

def extract_video_urls_from_thread(thread_url: str) -> list:
    """
    Extract all video URLs from a Twitter/X thread
    Returns a list of video URLs
    """
    # For now, we'll treat the thread URL itself as a video URL
    # In a real implementation, we would need to use Twitter's API
    # or web scraping to get all video URLs from the thread
    return [thread_url]

async def is_subscribed(update: Update, bot: Bot) -> bool:
    """
    Check if user is subscribed to the required channel
    """
    try:
        user_id = update.effective_user.id
        channel_id = os.environ["TELEGRAM_CHANNEL_ID"]
        
        # Get user's membership status
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        
        # Check if user is a member
        return member.status in ['member', 'administrator', 'creator']
    except TelegramError as e:
        print(f"Error checking subscription: {str(e)}")
        return False

def check_subscription(func):
    """
    Decorator to check channel subscription before executing command
    """
    async def wrapper(update: Update, context, *args, **kwargs):
        # Check if user is subscribed
        is_member = await is_subscribed(update, context.bot)
        
        if not is_member:
            channel_id = os.environ["TELEGRAM_CHANNEL_ID"]
            try:
                channel_info = await context.bot.get_chat(channel_id)
                channel_name = channel_info.title
                invite_link = channel_info.invite_link or "the channel"
                
                message = (
                    f"❌ You must subscribe to *{channel_name}* to use this bot!\n\n"
                    f"1. Join {invite_link}\n"
                    f"2. Come back and try again"
                )
            except TelegramError:
                message = (
                    "❌ You must subscribe to our channel to use this bot!\n\n"
                    "1. Join the required channel\n"
                    "2. Come back and try again"
                )
                
            await update.message.reply_text(message, parse_mode='Markdown')
            return
        
        # User is subscribed, proceed with the command
        return await func(update, context, *args, **kwargs)
    
    return wrapper
