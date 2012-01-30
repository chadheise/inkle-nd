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
    members = models.ManyToManyField("Member")
    
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

    def get_formatted_category(self):
        """Returns the current member's formatted category."""
        if (self.category == "dinner"):
            return "Dinner"
        elif (self.category == "pregame"):
            return "Pregame"
        elif (self.category == "mainEvent"):
            return "Main Event"


class Invitation(models.Model):
    """Invitation class definition."""
    description = models.CharField(max_length = 200)
    inkling = models.ForeignKey(Inkling)
    from_member = models.ForeignKey("Member")
    
    def __unicode__(self):
        """String representation for the current invitation."""
        return "%s - %s (%s)" % (self.inkling, self.from_member, self.description)


class ActiveMemberManager(models.Manager):
    """Manager which returns active member objects."""
    def get_query_set(self):
        return Member.objects.filter(is_active = True)


class Member(User):
    """Member class definition. Inherits from built-in Django User class."""
    circles = models.ManyToManyField(Circle)
    spheres = models.ManyToManyField(Sphere)
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
    city = models.CharField(max_length = 50, default = "")
    state = models.CharField(max_length = 2, default = "")
    zip_code = models.CharField(max_length = 5, default = "")

    # Inviations
    invitations = models.ManyToManyField(Invitation)

    # Email verification
    verification_hash = models.CharField(max_length = 32)
    verified = models.BooleanField(default = False)

    # Privacy settings
    location_privacy = models.IntegerField(max_length = 1, default = 0)
    email_privacy = models.IntegerField(max_length = 1, default = 1)
    phone_privacy = models.IntegerField(max_length = 1, default = 1)
    birthday_privacy = models.IntegerField(max_length = 1, default = 1)
    followers_privacy = models.IntegerField(max_length = 1, default = 2)
    followings_privacy = models.IntegerField(max_length = 1, default = 2)
    spheres_privacy = models.IntegerField(max_length = 1, default = 0)
    inklings_privacy = models.IntegerField(max_length = 1, default = 2)

    # Email preferences
    requested_email_preference = models.BooleanField(default = True)
    accepted_email_preference = models.BooleanField(default = True)
    invited_email_preference = models.BooleanField(default = True)
    general_email_preference = models.BooleanField(default = True)

    # Custom manager
    objects = models.Manager()
    active = ActiveMemberManager()

    # Note: inherits from built-in Django User class which contains:
    #       id, username, password, first_name, last_name, email, is_staff, is_active, is_superuser, last_login, and date_joined
   
    def __unicode__(self):
        """String representation for the current member."""
        return "%s (%s %s)" % (self.username, self.first_name, self.last_name)

    def get_absolute_url(self):
        """Returns the URL for the current member's member page."""
        return "/member/%i/" % (self.id)

    def get_formatted_phone(self):
        """Returns the current member's formatted phone number."""
        return "(%s) %s-%s" % (self.phone[0:3], self.phone[3:6], self.phone[6:10])

    def get_formatted_birthday(self):
        """Returns the current member's formatted birthday."""
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        birthday = self.birthday.split("/")
        return "%s %s, %s" % (months[int(birthday[0]) - 1], birthday[1], birthday[2])

    def update_verification_hash(self):
        """Updates the current member's verification hash."""
        self.verification_hash = md5(str(randint(1000, 9999))).hexdigest()

    def update_profile_information(self, first_name, last_name, phone, city, state, zip_code, birthday, gender):
        """Updates the current member's privacy settings."""
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.birthday = birthday
        self.gender = gender

    def update_privacy_settings(self, location, email, phone, birthday, followers, followings, spheres, inklings):
        """Updates the current member's privacy settings."""
        self.location_privacy = location
        self.email_privacy = email
        self.phone_privacy = phone
        self.birthday_privacy = birthday
        self.followers_privacy = followers
        self.followings_privacy = followings
        self.spheres_privacy = spheres
        self.inklings_privacy = inklings

    def update_email_preferences(self, requested, accepted, invited, general):
        """Updates the current member's email preferences."""
        self.requested_email_preference = requested
        self.accepted_email_preference = accepted
        self.invited_email_preference = invited
        self.general_email_preference = general
