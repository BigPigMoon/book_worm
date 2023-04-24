from telegram import Update
from telegram.ext import ContextTypes

import messages
import services
from .response import send_response


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user['id']
    services.registration(uid)
    await send_response(update, context, response=messages.GREETING)
