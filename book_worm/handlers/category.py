from telegram import Update
from telegram.ext import ContextTypes

import services
import config
import models

from .response import send_response
from .keyboard import get_category_keyboard, get_delete_category_keyboard, get_index_of_button


async def add_category_process(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user: models.User,
    user_message: str,
):
    models.Category.create(title=user_message, user=user)

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
    """Category button handler.

    Handel button pressed
    """

    query = update.callback_query

    await query.answer()

    if not query.data or not query.data.strip():
        return

    current_category_index_command = get_index_of_button(
        query.data, config.CATEGORIES_PATTERN
    )

    uid = update.callback_query.from_user.id
    user = services.user.get_current_user(uid)

    match current_category_index_command:
        case 1 if user:
            await send_response(
                update, context,
                "Укажите имя для новой категории",
            )
            user.is_add_category = True
            user.is_add_book = False
            user.save()
        case 2 if user:
            await send_response(
                update, context,
                "Какую категорию желаете удалить?",
                get_delete_category_keyboard(
                    config.DELETE_CATEGORY_PATTERN, user
                )
            )


async def delete_category_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete category button handler.

    Handel button pressed
    """

    query = update.callback_query

    await query.answer()

    if not query.data or not query.data.strip():
        return

    category_index = get_index_of_button(
        query.data, config.DELETE_CATEGORY_PATTERN
    )
    models.Category.delete_by_id(category_index)

    uid = update.callback_query.from_user.id
    user = services.user.get_current_user(uid)
    text = services.all_categories(user)

    await send_response(
        update, context, text,
        get_category_keyboard(config.CATEGORIES_PATTERN),
    )
