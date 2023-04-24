from peewee import SqliteDatabase, Model


db = SqliteDatabase('book_work.db')


class BaseModel(Model):
    class Meta:
        database = db
