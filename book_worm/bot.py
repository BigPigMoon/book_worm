"""Main bot module"""

import os
import logging

from dotenv import load_dotenv

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

import handlers
import models
import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger()

load_dotenv()

COMMAND_HANDLES = {
    "start": handlers.start_command,
    "help": handlers.help_command,
    "categories": handlers.category_command,
    "books": handlers.book_command,
}

CALLBACK_QUERY_HANDLES = {
    rf'^{config.CATEGORIES_PATTERN}(\d+)$': handlers.category_buttons,
    rf'^{config.DELETE_CATEGORY_PATTERN}(\d+)$': handlers.delete_category_buttons,
    rf'^{config.BOOKS_CAROUSEL_PATTERN}(\d+)$': handlers.book_buttons_carousel,
    rf'^{config.ADD_BOOK}$': handlers.add_book,
    rf'^{config.DELETE_BOOK}$': handlers.delete_book,
}

if __name__ == '__main__':
    models.database_create()

    application = ApplicationBuilder().token(
        os.getenv('TELEGRAM_BOT_TOKEN')
    ).build()

    for command_name, command_handler in COMMAND_HANDLES.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    for pattern, handler in CALLBACK_QUERY_HANDLES.items():
        application.add_handler(CallbackQueryHandler(handler, pattern=pattern))

    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND),
                       handlers.handle_message)
    )

    application.run_polling()
