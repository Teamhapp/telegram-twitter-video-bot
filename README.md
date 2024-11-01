# Twitter/X Video Downloader Telegram Bot

A Telegram bot that downloads and shares Twitter/X videos using Python. The bot supports downloading single videos and entire threads, with configurable video quality options.

## Features

- Download videos from Twitter/X posts
- Support for downloading videos from Twitter threads
- Configurable video quality options (best, medium, low)
- Force subscribe feature requiring users to join a specific channel
- Temporary file management to avoid storage issues

## Requirements

- Python 3.11+
- python-telegram-bot
- yt-dlp

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd twitter-video-downloader-bot
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id
```

## Usage

1. Start the bot:
```bash
python main.py
```

2. Available commands in Telegram:
- `/start` - Start the bot
- `/help` - Show help message
- `/quality` - Show current quality setting
- `/quality_best` - Set video quality to best
- `/quality_medium` - Set video quality to medium (480p)
- `/quality_low` - Set video quality to low (240p)

## Project Structure

```
├── main.py           # Main bot implementation
├── config.py         # Configuration settings
├── utils.py          # Utility functions
└── temp/            # Temporary directory for downloads
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
