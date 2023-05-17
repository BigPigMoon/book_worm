from datetime import datetime

from peewee import BigIntegerField, DateTimeField, BooleanField, IntegerField

from models.db import BaseModel


class User(BaseModel):
    telegram_id = BigIntegerField(unique=True)
    created_at = DateTimeField(default=datetime.now())

    is_add_category = BooleanField(default=False)
    is_add_book = BooleanField(default=False)
    selected_category = IntegerField(null=True, default=None)
