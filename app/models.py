import datetime
from app import db
from flask_login import UserMixin
from bson.objectid import ObjectId


class Dream(db.EmbeddedDocument):
    id_ = db.ObjectIdField(required=True, default=lambda: ObjectId())
    title = db.StringField(max_length=255, required=True, default="New Dream, New hope")
    estimated_time = db.IntField(min_value=1, required=True, default=40)
    current_time = db.IntField(required=True, default=0)

    def __unicode__(self):
        return self.title

    meta = {
        'ordering': ['title']
    }


class Month(db.EmbeddedDocument):
    id_ = db.ObjectIdField(required=True, default=lambda: ObjectId())
    title = db.StringField(max_length=255, required=True)
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
            self.title,
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

    def get_current_month(self):
        if self.months:
            for month in self.months:
                if month.n_month == datetime.datetime.today().month and \
                                month.year == datetime.datetime.today().year:
                    return month
            return self.months[0]
        return None

    meta = {
        'indexes': ['email'],
        'ordering': ['nickname']
    }
