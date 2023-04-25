from models import User, Book, Category


def get_books_by_category(user: User, category_id: int) -> str:
    """Get all categories from database"""

    try:
        category = Category.get_by_id(category_id)
    except Category.DoesNotExist:
        return 'Ты не добавил категории!'

    res = f'Книги в категории - <b>{category.title}</b>:\n\n'

    books = Book.select(Book.user == user and Book.category == category)
    if len(books) == 0:
        return res + 'Ты не добавил ни одну книжку в эту категорию!'

    for book in books:
        res += f'- {book.title}\n'

    return res
