from telegram import Update
from telegram.ext import ContextTypes

import messages
from .response import send_response


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_response(update, context, response=messages.HELP)
