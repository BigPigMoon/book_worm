from telegram import Update
from telegram.ext import ContextTypes

import services

from .response import send_response

from .category import add_category_process
from .book import add_book_process


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Message handler for add new category"""
    uid = update.message.from_user['id']
    user = services.user.get_current_user(uid)

    # print(user.is_add_category, user.is_add_book)
    if not user or not user.is_add_category and not user.is_add_book:
        await send_response(
            update, context,
            "Ты, по-моему, перепутал\nПосмотри справку /help"
        )
        return

    user_message = update.message.text

    if user.is_add_category:
        await add_category_process(update, context, user, user_message)
    elif user.is_add_book:
        await add_book_process(update, context, user, user_message)

    user.is_add_book = False
    user.is_add_category = False
    user.save()
