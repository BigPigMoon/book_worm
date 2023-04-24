from telegram import Update
from telegram.ext import ContextTypes

import services

from .response import send_response


async def category_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user['id']
    response = services.all_categories(uid)
    await send_response(update, context, response=response)
