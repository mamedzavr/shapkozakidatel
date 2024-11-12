import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from filter import FilterManager

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Create logger
logger = logging.getLogger(__name__)

# Create filter manager instance
filter_manager = FilterManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Привет! Я бот-фильтр. Используй команду /filter <слово> в ответ на сообщение, чтобы создать фильтр.'
    )

def main():
    """Start the bot."""
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        logger.error("No token found! Make sure to set TELEGRAM_TOKEN environment variable.")
        return

    # Create the Application
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("filter", filter_manager.add_filter))
    application.add_handler(CommandHandler("filters", filter_manager.show_filters))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_manager.check_message))

    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
