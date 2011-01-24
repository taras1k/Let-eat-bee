from mongoengine import *
from mongoengine.django.auth import User


# Create your models here.

class Reletionships(Document):
    username = ReferenceField(User)
    user_friend = ReferenceField(User)

class Places(Document):
    place_name = StringField(required = True)

class Events(Document):
    title = StringField(max_length=120, required=True)
    creator = ReferenceField(User)
    place = ReferenceField(Places)
    participent_number = IntField()

class EventParticioents(Document):
    event = ReferenceField(Events)
    participent = ReferenceField(User)

class SecurityJoinEvent(Document):
    event = ReferenceField(Events)
    permisions = IntField()

class SecurityCommentEvent(Document):
    event = ReferenceField(Events)
    permisions = IntField()

class SecurityViewProfile(Document):
    profile = ReferenceField(User)
    permisions = IntField()

class EventComment(Document):
    event = ReferenceField(Events)
    user  = ReferenceField(User)
    comment = StringField()

class EventFeedback(Document):
    event = ReferenceField(Events)
    user  = ReferenceField(User)
    comment = StringField()




