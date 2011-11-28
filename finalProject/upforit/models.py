from django.db import models
from django.contrib.auth.models import User

STATES = (
    ("AL", "Alabama"),
    ("AK", "Alaska"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KS", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MD", "Maryland"),
    ("MA", "Massachusetts"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PA", "Pennsylvania"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming"),
)

LOCATION_CATEGORIES = (
    ("Bar", "Bar"),
    ("Movie theater", "Movie theater"),
    ("Dorm", "Dorm"),
    ("Restaurant", "Restaurant"),
    ("Stadium", "Stadium"),
    ("Apartment complex", "Apartment complex"),
    ("Other", "Other"),
)

EVENT_CATEGORIES = (
    ("D", "Dinner"),
    ("P", "Pregame"),
    ("M", "Main event"),
)

GENDERS = (
    ("M", "Male"),
    ("F", "Female"),
)

class Location(models.Model):
    name = models.CharField(max_length = 100)
    category = models.CharField(max_length = 20, choices = LOCATION_CATEGORIES, default = "Other")
    street = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 2, choices = STATES, default = "AL")
    zip_code = models.IntegerField(max_length = 5)
    
    # image ???
    
    # hours ???
    # specials ???

    def __unicode__(self):
        return "%s (%s, %s)" % (self.name, self.city, self.state)

class Sphere(models.Model):
    name = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return "%s" % (self.name)

class Circle(models.Model):
    name = models.CharField(max_length = 50)
    member = models.ManyToManyField("Member")
    
    def __unicode__(self):
        return "%s" % (self.name)

class Follower(models.Model):
    follower = models.ForeignKey("Member")
    count = models.IntegerField()
    
    def __unicode__(self):
        return "%s (%d)" % (self.follower.username, count)

class Member(User):
    # User contains id, username, password, first_name, last_name, email, is_staff, is_active, is_superuser, last_login, and date_joined
    spheres = models.ManyToManyField(Sphere)
    circles = models.ManyToManyField(Circle, related_name = "+")

    pending = models.ManyToManyField("self")
    accepted = models.ManyToManyField("self")
    requested = models.ManyToManyField("self")
    followers = models.ManyToManyField(Follower)
    
    events = models.ManyToManyField(Event)

    gender = models.CharField(max_length = 1, choices = GENDERS, default = "M")
    phone = models.IntegerField(max_length = 10, default = "0000000000")
    # image ???
    
    def __unicode__(self):
        return "%s" % (self.username)

class Event(models.Model):
    location = models.ForeignKey(Location)
    category = models.CharField(max_length = 1, choices = EVENT_CATEGORIES, default = "D")
    date = models.DateField(auto_now_add = True)
    
    def __unicode__(self):
        return "%s, %s (%s)" % (self.member.username, self.location.name, self.date)
