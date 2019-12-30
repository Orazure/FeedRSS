from peewee import *
from flask_login import UserMixin
import wtforms
from wtfpeewee.orm import model_form




database = SqliteDatabase("myfeed.sqlite3")

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel,UserMixin):
    user_id=AutoField(primary_key=True)
    user_username = CharField(null=True)
    user_password = CharField(null=True)
    
    
def create_tables():
    with database:
        database.create_tables([User])

def drop_tables():
    with database:
        database.drop_tables([User])
