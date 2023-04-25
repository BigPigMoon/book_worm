from models import User, Category


def all_categories(user: User) -> str:
    """Get all categories from database"""

    categories = Category.select().where(Category.user == user)

    if len(categories) == 0:
        return 'Ты не добавил ни одну категорию! Добавь быстро!'

    res = 'Ваши категории:\n'

    for category in categories:
        res += f'- {category.title}\n'

    return res
