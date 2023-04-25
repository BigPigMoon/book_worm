from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from models import Category, User
import config


def get_category_keyboard(callback_prefix: str) -> InlineKeyboardMarkup:
    """Return keyboard for show category list"""

    keyboard = [[
        InlineKeyboardButton(
            'Новая категория',
            callback_data=f'{callback_prefix}1'
        ),
        InlineKeyboardButton(
            'Удалить категорию',
            callback_data=f'{callback_prefix}2',
        ),
    ]]

    return InlineKeyboardMarkup(keyboard)


def get_delete_category_keyboard(callback_prefix: str, user: User) -> InlineKeyboardMarkup:
    """Return keyboard for delete category"""

    categories = Category.select().where(Category.user == user)

    keyboard = [
        [InlineKeyboardButton(
            category.title, callback_data=f'{callback_prefix}{category.id}'
        )] for category in categories
    ]

    return InlineKeyboardMarkup(keyboard)


def get_book_keyboard(
    current_category_index: int,
    categories_count: int,
    callback_prefix: str
) -> InlineKeyboardMarkup:
    """Return keyboard for move between categories"""
    if categories_count == 0:
        return InlineKeyboardMarkup([[]])

    prev_index = current_category_index - 1
    if prev_index < 0:
        prev_index = categories_count - 1

    next_index = current_category_index + 1
    if next_index > categories_count - 1:
        next_index = 0

    keyboard = [
        [
            InlineKeyboardButton(
                "<-", callback_data=f'{callback_prefix}{prev_index}'),
            InlineKeyboardButton(
                f'{current_category_index + 1}/{categories_count}', callback_data=' '),
            InlineKeyboardButton(
                "->", callback_data=f'{callback_prefix}{next_index}'),
        ],
        [InlineKeyboardButton(
            'Добавить новую книжку в эту категорию',
            callback_data=f'{config.ADD_BOOK}',
        ),],
        [InlineKeyboardButton(
            'Удалить книжку из этой категории',
            callback_data=f'{config.DELETE_BOOK}',
        ),],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_index_of_button(query_data, pattren_prefix: str) -> int:
    pattern_prefix_length = len(pattren_prefix)
    return int(query_data[pattern_prefix_length:])
