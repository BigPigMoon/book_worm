import logging

from models import User, Category


logger = logging.getLogger()


def all_categories(uid: str) -> str:
    """Get all categories from database"""
    if not uid:
        logger.warning("User id does not exist")
        return "Я вас не узнаю!"

    user: User
    try:
        user = User.select().where(User.telegram_id == uid).get()
    except User.DoesNotExist:
        user = None

    res = ""
    if user:
        for category in Category.select().where(Category.user == user):
            res += category.title + "\n"

    if len(res) == 0:
        res = "Вы не добавили ни одну категорию."

    return res
