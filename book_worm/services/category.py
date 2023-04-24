import logging

from models import User, Category


logger = logging.getLogger()


def all_categories(user: User) -> str:
    """Get all categories from database"""

    categories = Category.select().where(Category.user == user)

    if len(categories) == 0:
        return ''

    res = 'Ваши категории:\n'

    for category in categories:
        res += f'- {category.title}\n'

    return res
