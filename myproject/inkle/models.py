from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length = 100)
    image = models.CharField(max_length = 100, default = "default.jpg")
    category = models.CharField(max_length = 20, default = "Other")
    
    # Address
    street = models.CharField(max_length = 50, default = "")
    city = models.CharField(max_length = 50, default = "")
    state = models.CharField(max_length = 2, default = "")
    zip_code = models.CharField(max_length = 5, default = "")
    
    # Contact info
    phone = models.CharField(max_length = 10, default = "")
    website = models.CharField(max_length = 100, default = "")

    def __unicode__(self):
        return "%s (%s, %s)" % (self.name, self.city, self.state)

class Sphere(models.Model):
    name = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return "%s" % (self.name)

class Circle(models.Model):
    name = models.CharField(max_length = 50)
    members = models.ManyToManyField("Member", symmetrical = False)
    
    def __unicode__(self):
        return "%s" % (self.name)

class Follower(models.Model):
    follower = models.ForeignKey("Member")
    count = models.IntegerField()
    
    def __unicode__(self):
        return "%s (%d)" % (self.follower.username, self.count)

class Inkling(models.Model):
    location = models.ForeignKey(Location)
    category = models.CharField(max_length = 1)
    date = models.CharField(max_length = 10)
    
    def __unicode__(self):
        return "%s (%s, %s)" % (self.location.name, self.date, self.category)

class Member(User):
    # User contains id, username, password, first_name, last_name, email, is_staff, is_active, is_superuser, last_login, and date_joined

    spheres = models.ManyToManyField(Sphere, symmetrical = False)
    circles = models.ManyToManyField(Circle, symmetrical = False, related_name = "+")

    pending = models.ManyToManyField("self", symmetrical = False, related_name = "++")
    accepted = models.ManyToManyField("self", symmetrical = False, related_name = "+++")
    requested = models.ManyToManyField("self", symmetrical = False, related_name = "++++")
    followers = models.ManyToManyField(Follower, symmetrical = False)
    following = models.ManyToManyField("self", symmetrical = False)
    
    inklings = models.ManyToManyField(Inkling)

    gender = models.CharField(max_length = 6)
    birthday = models.CharField(max_length = 14)
    phone = models.CharField(max_length = 10, default = "")
    image = models.CharField(max_length = 100, default = "default.jpg")
    
    # Address
    city = models.CharField(max_length = 50, default = "")
    state = models.CharField(max_length = 2, default = "")
    zip_code = models.CharField(max_length = 5, default = "")
    
    def __unicode__(self):
        return "%s" % (self.username)
