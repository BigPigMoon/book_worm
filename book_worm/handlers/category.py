import telegram
from telegram import Update
from telegram.ext import ContextTypes

import services
import config
import models

from .response import send_response
from .keyboard import get_category_keyboard


async def add_category_process(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Message handler for add new category"""

    uid = update.message.from_user['id']
    user = services.user.get_current_user(uid)

    if not user or not user.is_add_category:
        await send_response(
            update, context,
            "Ты, по-моему, перепутал\nПосмотри справку /help"
        )
        return

    user_message = update.message.text

    models.Category.create(title=user_message, user=user)
    user.is_add_category = False
    user.save()

    response = services.all_categories(user)

    await send_response(
        update, context,
        response=response,
        keyboard=get_category_keyboard(config.CATEGORIES_PATTERN)
    )


async def category_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user['id']
    user = services.get_current_user(uid)
    response = services.all_categories(user)

    await send_response(
        update, context,
        response=response,
        keyboard=get_category_keyboard(config.CATEGORIES_PATTERN)
    )


async def category_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if not query.data or not query.data.strip():
        return

    uid = update.callback_query.from_user.id

    user = services.user.get_current_user(uid)

    current_category_index_command = _get_current_category_index(query.data)

    if current_category_index_command == 1 and user:
        await send_response(
            update, context,
            "Укажите имя для новой категории",
        )
        user.is_add_category = True
        user.save()


def _get_current_category_index(query_data) -> int:
    pattern_prefix_length = len(config.CATEGORIES_PATTERN)
    return int(query_data[pattern_prefix_length:])
