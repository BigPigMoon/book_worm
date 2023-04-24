from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def get_category_keyboard(callback_prefix: str):
    keyboard = [[
        InlineKeyboardButton(
            'Новая категория.',
            callback_data=f'{callback_prefix}1'
        )
    ]]

    return InlineKeyboardMarkup(keyboard)
