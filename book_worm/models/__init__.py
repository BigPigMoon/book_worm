from .book import Book
from .db import database
from .user import User
from .category import Category


def database_create():
    with database:
        database.create_tables([
            User,
            Category,
            Book,
        ])
