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
