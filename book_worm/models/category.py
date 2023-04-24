from datetime import datetime

from peewee import DateTimeField, ForeignKeyField, TextField

from models.db import BaseModel
from models.user import User


class Category(BaseModel):
    created_at = DateTimeField(default=datetime.now())
    title = TextField()

    user = ForeignKeyField(User, backref="categories")
