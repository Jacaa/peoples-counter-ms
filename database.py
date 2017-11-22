import config
from peewee import *

# Get database settings
dbname = config.DB_NAME
user = config.DB_USERNAME
password = config.DB_PASSWORD

# Set database instance
db = PostgresqlDatabase(dbname, user=user, password=password)

# Database tables
class Users(Model):
    email = CharField()
    admin = BooleanField()
    save_photo = BooleanField()
    send_notification = BooleanField()

    class Meta:
      database = db

class Events(Model):
    walked_in = BooleanField()
    photo = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    
    class Meta:
      database = db
