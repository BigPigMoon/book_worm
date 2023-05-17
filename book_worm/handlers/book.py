import telegram
from telegram import Update
from telegram.ext import ContextTypes

import config
import services
import models

from .response import send_response
from .keyboard import get_book_keyboard, get_index_of_button


async def add_book_process(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user: models.User,
    user_message: str,
):
    """Message handler for add new book"""

    category = models.Category.get_by_id(user.selected_category)

    # print(category.title)

    await book_command(update, context)


async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user['id']
    user = services.get_current_user(uid)

    categories = list(models.Category.select().where(
        models.category.Category.user == user))

    if len(categories) > 0:
        print(user.selected_category)
        if user.selected_category is None:
            user.selected_category = categories[0]
            user.save()

        text = services.get_books_by_category(user, user.selected_category)
    else:
        text = 'Ты не добавил категории!'

    await send_response(
        update, context,
        text,
        get_book_keyboard(0, len(categories), config.BOOKS_CAROUSEL_PATTERN)
    )


async def book_buttons_carousel(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if not query.data or not query.data.strip():
        return

    current_category_index = get_index_of_button(
        query.data, config.BOOKS_CAROUSEL_PATTERN
    )

    uid = update.callback_query.from_user.id
    user = services.user.get_current_user(uid)
    categories = list(models.Category.select().where(
        models.category.Category.user == user))
    user.selected_category = categories[current_category_index].id
    user.save()

    await query.edit_message_text(
        text=services.get_books_by_category(
            user, user.selected_category
        ),
        reply_markup=get_book_keyboard(
            current_category_index,
            len(categories),
            config.BOOKS_CAROUSEL_PATTERN
        ),
        parse_mode=telegram.constants.ParseMode.HTML
    )


async def add_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if not query.data or not query.data.strip():
        return

    uid = update.callback_query.from_user.id
    user = services.user.get_current_user(uid)
    categories = list(models.Category.select().where(
        models.category.Category.user == user))

    await send_response(
        update, context,
        "Укажи имя для новой книжки",
    )
    user.is_add_category = False
    user.is_add_book = True
    user.save()


async def delete_book(update: Update, _: ContextTypes.DEFAULT_TYPE):
    pass
