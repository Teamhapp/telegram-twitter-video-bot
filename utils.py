import os
import re
import uuid
from urllib.parse import urlparse
from config import TWITTER_URL_PATTERNS, TEMP_DIR

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
