#from django.db import models

#from django.contrib.auth import authenticate
from mongoengine import *
from mongoengine.django.auth import User
from mongoengine.django.auth import MongoEngineBackend
import datetime
#from django.contrib.sites.models import Site 

class FacebookProfile(Document):
    user = ReferenceField(User)
    #site = models.ForeignKey(Site, default=Site.objects.get_current)
    uid = StringField(max_length=255, required = True)
    
    def __unicode__(self):
        return u'%s: %s' % (self.user, self.uid)
    
    def authenticate(self):
        return get_user(uid=self.uid)

class TwitterProfile(Document):
    user = ReferenceField(User)
    #site = models.ForeignKey(Site, default=Site.objects.get_current)
    twitter_id = IntField()
    
    def __unicode__(self):
        return u'%s: %s' % (self.user, self.twitter_id)
    
    def authenticate(self):
        return get_user(twitter_id=self.twitter_id)

class OpenIDProfile(Document):
    user = ReferenceField(User)
    #site = models.ForeignKey(Site, default=Site.objects.get_current)
    identity = StringField()
    
    def __unicode__(self):
        return u'OpenID Profile for %s, via provider %s' % (self.user, self.identity)

    def authenticate(self):
        return get_user(identity=self.identity)

class OpenIDStore(Document):
   # site = models.ForeignKey(Site, default=Site.objects.get_current)
    server_url = StringField(max_length=255)
    handle = StringField(max_length=255)
    secret = StringField()
    issued = IntField()
    lifetime = IntField()
    assoc_type = StringField()

    def __unicode__(self):
        return u'OpenID Store %s for %s' % (self.server_url, self.site)

class OpenIDNonce(Document):
    server_url = StringField(max_length=255)
    timestamp =  IntField()
    salt = StringField(max_length=255)
    date_created = DateTimeField(default = datetime.datetime.now())

    def __unicode__(self):
        return u'OpenID Nonce for %s' % self.server_url
