from datetime import datetime

from peewee import BigIntegerField, DateTimeField

from models.db import BaseModel


class User(BaseModel):
    telegram_id = BigIntegerField(unique=True)
    created_at = DateTimeField(default=datetime.now())
