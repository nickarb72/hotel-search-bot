from datetime import datetime

import peewee as pw


db = pw.SqliteDatabase('history.db')

class ModelBase(pw.Model):
    class Meta():
        database = db

class History(ModelBase):
    record_id = pw.AutoField(primary_key=True)
    chat_id = pw.IntegerField()
    created_at = pw.DateField(default=datetime.now())
    name = pw.TextField()
    url = pw.TextField()
    description = pw.TextField()
    price_per_night = pw.FloatField()
    latitude = pw.FloatField()
    longitude = pw.FloatField()

class Photos(ModelBase):
    url = pw.TextField()
    hotel = pw.ForeignKeyField(History, backref='photos')