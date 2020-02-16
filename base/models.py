from peewee import *
import datetime 
from flask_login import UserMixin
import wtforms
from wtfpeewee.orm import model_form


database = SqliteDatabase("myfeed.sqlite3")


class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel,UserMixin):

    user_id=IntegerField(primary_key=True)
    user_username = CharField(null=True)
    user_password = CharField(null=True)

    def is_active(self):
        """True, as all users are active."""
        return True
        
    def is_authenticated(self):
        return True

    def get_username(self):
        return self.user_id

    def get_id(self):
        return self.user_id

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
  
    
class feed(BaseModel):
    feed_nom=CharField(null=True)
    feed_url=CharField(null=True)
    feed_date = DateTimeField(default=datetime.datetime.now,null=True)
    user_feed = CharField(null=True)




def create_tables():
    with database:
        database.create_tables([feed])

def drop_tables():
    with database:
        database.drop_tables([feed])
