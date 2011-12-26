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
    ("Club", "Club"),
    ("Movie theater", "Movie theater"),
    ("Dorm", "Dorm"),
    ("Restaurant", "Restaurant"),
    ("Stadium", "Stadium"),
    ("Apartment complex", "Apartment complex"),
    ("Other", "Other"),
)

class Location(models.Model):
    name = models.CharField(max_length = 100)
    image = models.CharField(max_length = 100, default = "default.jpg")
    
    # Address
    category = models.CharField(max_length = 20, default = "Other")
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
    
    def __unicode__(self):
        return "%s" % (self.username)
