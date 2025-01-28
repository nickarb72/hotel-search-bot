from database.common.models import db, History, Photos

db.connect()
db.create_tables([History, Photos])

