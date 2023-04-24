"""Main bot module"""

import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import messages
import services
from models import db, user

logging.basicConfig(
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    level=logging.INFO
)

logger = logging.getLogger()

load_dotenv()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning("effective_chat is None in /start")
        return

    services.user.registration(update.message.from_user['id'])

    await context.bot.send_message(
        chat_id=effective_chat.id,
        text=messages.GREETING,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning("effective_chat is None in /help")
        return

    await context.bot.send_message(
        chat_id=effective_chat.id,
        text=messages.HELP,
    )


async def category_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning("effective_chat is None in /categories")
        return

    await context.bot.send_message(
        chat_id=effective_chat.id,
        text="",
    )

if __name__ == '__main__':
    with db.db:
        db.db.create_tables([user.User,])

    application = ApplicationBuilder().token(
        os.getenv('TELEGRAM_BOT_TOKEN')
    ).build()

    start_handler = CommandHandler('start', start_command)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help_command)
    application.add_handler(help_handler)

    application.run_polling()
