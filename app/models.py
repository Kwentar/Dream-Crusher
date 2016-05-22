import datetime
from app import db
from flask_login import UserMixin


class Dream(db.Document):
    created_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    estimated_time = db.IntField(min_value=1, required=False)
    current_time = db.IntField(required=True, default=0)

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_time'],
        'ordering': ['title']
    }


class Month(db.Document):
    name = db.StringField(max_length=255, required=True)
    year = db.IntField(min_value=datetime.datetime.today().year, required=True, default=datetime.datetime.today().year)
    n_month = db.IntField(min_value=1, max_value=12, required=True)
    slogan = db.StringField(max_length=640, required=True, default="I'm so lazy to come up with something")
    dreams = db.ListField(db.EmbeddedDocumentField('Dream'))
    meta = {
        'indexes': ['n_month', 'year'],
        'ordering': ['year', 'n_month']
    }

    def __unicode__(self):
        return "{} of {} with slogan {}, Dreams: {}".format(
            self.name,
            self.year,
            self.slogan,
            ",".join([x.title for x in self.dreams]))

ROLE_ADMIN = 0
ROLE_USER = 1


class User(db.Document, UserMixin):
    nickname = db.StringField(max_length=255, required=True)
    email = db.EmailField(max_length=255, required=True, unique=True, primary_key=True)
    role = db.IntField(required=True, default=ROLE_USER)
    avatar_url = db.StringField(required=True, defaul="")
    months = db.ListField(db.EmbeddedDocumentField('Month'))

    def __unicode__(self):
        return "{} {} {}, Months: {}".format(
            self.nickname,
            self.email,
            "user" if self.role else "admin",
            ",".join([x.title for x in self.months]))

    def get_id(self):
        return str(self.email)

    meta = {
        'indexes': ['email'],
        'ordering': ['nickname']
    }
