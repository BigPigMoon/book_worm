from datetime import datetime

from peewee import DateTimeField, TextField, ForeignKeyField

from models.db import BaseModel
from models.user import User
from models.category import Category


class Book(BaseModel):
    created_at = DateTimeField(default=datetime.now())
    title = TextField()
    filename = TextField()
    read_start = DateTimeField()
    read_finish = DateTimeField()

    category = ForeignKeyField(Category, backref="books")
    user = ForeignKeyField(User, backref='books')
