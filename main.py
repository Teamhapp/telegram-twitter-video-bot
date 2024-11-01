import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import (
    BOT_TOKEN, WELCOME_MESSAGE, HELP_MESSAGE, 
    VIDEO_QUALITIES, DEFAULT_QUALITY
)
from utils import (
    is_valid_twitter_url, generate_temp_filename, cleanup_temp_file, 
    ensure_temp_dir_exists, is_thread_url, extract_video_urls_from_thread
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    await update.message.reply_text(WELCOME_MESSAGE)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    await update.message.reply_text(HELP_MESSAGE, parse_mode='Markdown')

async def quality_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current quality setting"""
    quality = context.user_data.get('quality', DEFAULT_QUALITY)
    message = f"Current video quality: *{quality}* ({VIDEO_QUALITIES[quality]})"
    await update.message.reply_text(message, parse_mode='Markdown')

async def set_quality(update: Update, context: ContextTypes.DEFAULT_TYPE, quality: str):
    """Set video quality preference"""
    if quality not in VIDEO_QUALITIES:
        await update.message.reply_text("❌ Invalid quality setting.")
        return
    
    context.user_data['quality'] = quality
    message = f"✅ Video quality set to: *{quality}* ({VIDEO_QUALITIES[quality]})"
    await update.message.reply_text(message, parse_mode='Markdown')

async def quality_best_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_quality(update, context, 'best')

async def quality_medium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_quality(update, context, 'medium')

async def quality_low_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_quality(update, context, 'low')

def get_format_options(quality: str) -> dict:
    """Get yt-dlp format options based on quality setting"""
    formats = {
        'best': 'best',
        'medium': 'best[height<=480]',
        'low': 'best[height<=240]'
    }
    return {'format': formats.get(quality, 'best')}

async def download_video(url: str, quality: str = DEFAULT_QUALITY) -> str:
    """
    Download video from Twitter/X URL
    Returns the path to the downloaded file
    """
    output_file = generate_temp_filename()
    
    format_opts = get_format_options(quality)
    ydl_opts = {
        'outtmpl': output_file,
        'quiet': True,
        **format_opts
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_file
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        raise

async def handle_thread(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    """Handle Twitter/X thread URLs"""
    quality = context.user_data.get('quality', DEFAULT_QUALITY)
    status_message = await update.message.reply_text(
        f"⏳ Processing thread... This might take a while. Using {quality} quality."
    )
    
    try:
        # Get all video URLs from the thread
        video_urls = extract_video_urls_from_thread(url)
        
        if not video_urls:
            await update.message.reply_text("❌ No videos found in this thread.")
            return
        
        await status_message.edit_text(f"📥 Found {len(video_urls)} videos. Downloading...")
        
        # Download each video
        for i, video_url in enumerate(video_urls, 1):
            try:
                video_path = await download_video(video_url, quality)
                await update.message.reply_video(
                    video=open(video_path, 'rb'),
                    caption=f"✅ Video {i}/{len(video_urls)} from thread"
                )
                cleanup_temp_file(video_path)
            except Exception as e:
                await update.message.reply_text(
                    f"❌ Failed to download video {i}/{len(video_urls)}. Error: {str(e)}"
                )
                
        await update.message.reply_text("✅ Thread processing completed!")
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Sorry, I couldn't process this thread. Error: {str(e)}"
        )
        logger.error(f"Error processing thread {url}: {str(e)}")
    
    finally:
        await status_message.delete()

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming Twitter/X URLs"""
    url = update.message.text.strip()
    quality = context.user_data.get('quality', DEFAULT_QUALITY)
    
    if not is_valid_twitter_url(url):
        await update.message.reply_text(
            "❌ Please send a valid Twitter/X video URL."
        )
        return
    
    # Check if it's a thread URL
    if is_thread_url(url):
        await handle_thread(update, context, url)
        return
    
    # Handle single video
    status_message = await update.message.reply_text(
        f"⏳ Downloading video in {quality} quality... Please wait."
    )
    
    try:
        # Download the video
        video_path = await download_video(url, quality)
        
        # Send the video
        await update.message.reply_video(
            video=open(video_path, 'rb'),
            caption=f"✅ Here's your video in {quality} quality!"
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Sorry, I couldn't download this video. Error: {str(e)}"
        )
        logger.error(f"Error processing URL {url}: {str(e)}")
    
    finally:
        # Clean up
        await status_message.delete()
        if 'video_path' in locals():
            cleanup_temp_file(video_path)

def main():
    """Main function to run the bot"""
    # Ensure temp directory exists
    ensure_temp_dir_exists()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("quality", quality_command))
    application.add_handler(CommandHandler("quality_best", quality_best_command))
    application.add_handler(CommandHandler("quality_medium", quality_medium_command))
    application.add_handler(CommandHandler("quality_low", quality_low_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    
    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
