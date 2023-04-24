"""Main bot module"""

import os
import logging

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

import handlers
import models

logging.basicConfig(
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    level=logging.INFO
)

logger = logging.getLogger()

load_dotenv()

COMMAND_HANDLERS = {
    "start": handlers.start_command,
    "help": handlers.help_command,
    "categories": handlers.category_command,
}

if __name__ == '__main__':
    models.database_create()
    application = ApplicationBuilder().token(
        os.getenv('TELEGRAM_BOT_TOKEN')
    ).build()

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    application.run_polling()
