from django.db import models
from django.contrib.auth.models import User

# Import modules necessary for generating a new verification hash
from hashlib import md5
from random import randint

class Location(models.Model):
    """Location class definition."""
    # General information
    name = models.CharField(max_length = 100)
    image = models.CharField(max_length = 100, default = "default.jpg") # TODO: change default to ""?
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
        """String representation for the current location."""
        return "%s (%s, %s)" % (self.name, self.city, self.state)

    def get_absolute_url(self):
        """Returns the URL for the current location."""
        return "/location/%i/" % (self.id)

    def get_formatted_phone(self):
        """Returns the current location's formatted phone number."""
        return "(%s) %s-%s" % (self.phone[0:3], self.phone[3:6], self.phone[6:10])


class Sphere(models.Model):
    """Sphere class definition."""
    name = models.CharField(max_length = 50)
    
    def __unicode__(self):
        """String representation for the current sphere."""
        return "%s" % (self.name)

    def get_absolute_url(self):
        """Returns the URL for current sphere's sphere page."""
        return "/sphere/%i/" % (self.id)


class Circle(models.Model):
    """Circle class definition."""
    name = models.CharField(max_length = 50)
    members = models.ManyToManyField("Member", symmetrical = False)
    
    def __unicode__(self):
        """String representation for the current circle."""
        return "%s" % (self.name)


class Inkling(models.Model):
    """Inkling class definition."""
    location = models.ForeignKey(Location)
    category = models.CharField(max_length = 20)
    date = models.CharField(max_length = 10)
    
    def __unicode__(self):
        """String representation for the current inkling."""
        return "%s (%s, %s)" % (self.location.name, self.date, self.category)


class Member(User):
    """Member class definition. Inherits from built-in Django User class."""
    circles = models.ManyToManyField(Circle, symmetrical = False)
    spheres = models.ManyToManyField(Sphere, symmetrical = False)
    inklings = models.ManyToManyField(Inkling)

    # Member lists
    pending = models.ManyToManyField("self", symmetrical = False, related_name = "pending_related")
    accepted = models.ManyToManyField("self", symmetrical = False, related_name = "accepted_related")
    requested = models.ManyToManyField("self", symmetrical = False, related_name = "requested_related")
    followers = models.ManyToManyField("self", symmetrical = False, related_name = "followers_related")
    following = models.ManyToManyField("self", symmetrical = False, related_name = "following_related")
    
    # Profile information
    gender = models.CharField(max_length = 6)
    birthday = models.CharField(max_length = 10)
    phone = models.CharField(max_length = 10, default = "")
    image = models.CharField(max_length = 100, default = "default.jpg") # TODO: change default to ""?
    city = models.CharField(max_length = 50, default = "")
    state = models.CharField(max_length = 2, default = "")
    zip_code = models.CharField(max_length = 5, default = "")
    
    # Email verification
    verification_hash = models.CharField(max_length = 32, default = md5(str(randint(1000, 9999))).hexdigest())
    verified = models.BooleanField(default = False)

    # Note: inherits from built-in Django User class which contains:
    #       id, username, password, first_name, last_name, email, is_staff, is_active, is_superuser, last_login, and date_joined
   
    def __unicode__(self):
        """String representation for the current member."""
        return "%s (%s %s)" % (self.username, self.first_name, self.last_name)

    def get_absolute_url(self):
        """Returns the URL for the current member's member page."""
        return "/member/%i/" % (self.id)

    def get_full_name(self):
        """Returns the current member's full name."""
        return "%s %s" % (self.first_name, self.last_name)
    
    def get_formatted_phone(self):
        """Returns the current member's formatted phone number."""
        return "(%s) %s-%s" % (self.phone[0:3], self.phone[3:6], self.phone[6:10])

    def update_verification_hash(self):
        """Updates the current member's verification hash."""
        self.verification_hash = md5(str(randint(1000, 9999))).hexdigest()
