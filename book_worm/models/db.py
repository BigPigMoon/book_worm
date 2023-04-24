from peewee import SqliteDatabase, Model


database = SqliteDatabase('book_work.db')


class BaseModel(Model):
    class Meta:
        database = database
