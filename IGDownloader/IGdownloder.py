import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from instaloader import Instaloader, Post
from tqdm import tqdm
import requests

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Initialize Instaloader
L = Instaloader()

# Bot token (replace with your actual bot token)
BOT_TOKEN = "BOT_TOKEN"

# Rate limiting (store user download counts in memory; use a database for persistence)
user_download_counts = {}

# Maximum downloads per user per day
MAX_DOWNLOADS_PER_DAY = 15

# Helper function: Check rate limit
def check_rate_limit(user_id):
    if user_id not in user_download_counts:
        user_download_counts[user_id] = 0
    if user_download_counts[user_id] >= MAX_DOWNLOADS_PER_DAY:
        return False
    user_download_counts[user_id] += 1
    return True

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Send me an Instagram link to download media.\nUse /help for more commands."
    )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Available commands:
    /start - Start the bot and get instructions.
    /help - Display this help message.
    /download [link] - Download media from the provided Instagram link.
    /settings - Configure user preferences.
    /report [message] - Report a bug or issue.
    """
    await update.message.reply_text(help_text)

# Settings command
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings_text = "Settings:\n1. Download Format: [ZIP/Individual]\n2. Notifications: [On/Off]"
    await update.message.reply_text(settings_text)

# Bug reporting command
async def report_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bug_report = " ".join(context.args)
    if not bug_report:
        await update.message.reply_text("Please provide a bug description.")
        return
    admin_chat_id = "7916046473"  # Replace with your admin chat ID
    await context.bot.send_message(chat_id=admin_chat_id, text=f"Bug Report: {bug_report}")
    await update.message.reply_text("Thank you for reporting the bug!")

# Download media handler
async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    url = update.message.text.strip()

    # Check rate limit
    if not check_rate_limit(user_id):
        await update.message.reply_text("You have reached the daily download limit.")
        return

    # Validate URL
    if not url.startswith("https://www.instagram.com/"):
        await update.message.reply_text("Invalid link. Please send a valid Instagram URL.")
        return

    try:
        # Extract shortcode from URL
        shortcode = url.split("/")[-2]
        post = Post.from_shortcode(L.context, shortcode)

        # Progress bar for downloading
        def progress_bar(iterable, total_size):
            progress = tqdm(total=total_size, unit="B", unit_scale=True)
            for data in iterable:
                progress.update(len(data))
                yield data
            progress.close()

        # Handle media download
        if post.is_video:
            video_url = post.video_url
            response = requests.get(video_url, stream=True)
            file_path = f"{shortcode}.mp4"
            with open(file_path, "wb") as f:
                for chunk in progress_bar(response.iter_content(chunk_size=1024), int(response.headers.get("content-length", 0))):
                    f.write(chunk)
            await update.message.reply_video(open(file_path, "rb"))
            os.remove(file_path)
        else:
            for index, node in enumerate(post.get_sidecar_nodes()):
                if node.is_video:
                    video_url = node.video_url
                    response = requests.get(video_url, stream=True)
                    file_path = f"{shortcode}_{index}.mp4"
                    with open(file_path, "wb") as f:
                        for chunk in progress_bar(response.iter_content(chunk_size=1024), int(response.headers.get("content-length", 0))):
                            f.write(chunk)
                    await update.message.reply_video(open(file_path, "rb"))
                    os.remove(file_path)
                else:
                    image_url = node.display_url
                    response = requests.get(image_url, stream=True)
                    file_path = f"{shortcode}_{index}.jpg"
                    with open(file_path, "wb") as f:
                        for chunk in progress_bar(response.iter_content(chunk_size=1024), int(response.headers.get("content-length", 0))):
                            f.write(chunk)
                    await update.message.reply_photo(open(file_path, "rb"))
                    os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Error handler
async def handle_errors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error_message = f"An error occurred: {context.error}"
    await update.message.reply_text(error_message)

# Main function
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("report", report_bug))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    # Error handler
    application.add_error_handler(handle_errors)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()