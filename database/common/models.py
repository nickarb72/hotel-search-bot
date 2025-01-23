from datetime import datetime

import peewee as pw


db = pw.SqliteDatabase('history.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta():
        database = db


class History(ModelBase):
    name = pw.TextField()
    url = pw.TextField()
    description = pw.TextField()
    price_per_night = pw.FloatField()
    # photos = pw.
    latitude = pw.FloatField()
    longitude = pw.FloatField()