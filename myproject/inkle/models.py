from django.db import models
from django.contrib.auth.models import User

from hashlib import md5
from random import randint

import datetime

class ActiveLocationManager(models.Manager):
    """Manager which returns active location objects."""
    def get_query_set(self):
        return Location.objects.filter(is_active = True)


class Location(models.Model):
    """Location class definition."""
    # General information
    name = models.CharField(max_length = 100)
    category = models.CharField(max_length = 20, default = "Other")
    
    # Address
    street = models.CharField(max_length = 50, default = "")
    city = models.CharField(max_length = 50, default = "")
    state = models.CharField(max_length = 2, default = "")
    zip_code = models.CharField(max_length = 5, default = "")
    
    # Contact info
    phone = models.CharField(max_length = 10, default = "")
    website = models.CharField(max_length = 100, default = "")
    
    # Whether or not location is still open
    is_active =  models.BooleanField(default = True)

    # Managers
    objects = models.Manager()
    active = ActiveLocationManager()

    # Metadata
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        """String representation for the current location."""
        return "%s (%s, %s)" % (self.name, self.city, self.state)

    def get_absolute_url(self):
        """Returns the URL for the current location."""
        return "/location/%i/" % (self.id)

    def get_formatted_phone(self):
        """Returns the current location's formatted phone number."""
        return "(%s) %s-%s" % (self.phone[0:3], self.phone[3:6], self.phone[6:10])

    def __unicode__(self):
        """String representation for the current location."""
        return "%s (%s, %s)" % (self.name, self.city, self.state)

class Network(models.Model):
    """Network class definition."""
    name = models.CharField(max_length = 50)
    
    #Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        """String representation for the current network."""
        return "%s" % (self.name)

    def get_absolute_url(self):
        """Returns the URL for current network's network page."""
        return "/network/%i/" % (self.id)


class Blot(models.Model):
    """Blot class definition."""
    name = models.CharField(max_length = 50)
    members = models.ManyToManyField("Member")
    
    def __unicode__(self):
        """String representation for the current blot."""
        return "%s" % (self.name)


class PastInklingManager(models.Manager):
    """Manager which returns past inkling objects."""
    def get_query_set(self):
        return Inkling.objects.filter(date__lt = datetime.date.today())


class CurrentInklingManager(models.Manager):
    """Manager which returns current inkling objects."""
    def get_query_set(self):
        return Inkling.objects.filter(date__gte = datetime.date.today())


class Inkling(models.Model):
    """Inkling class definition."""
    location = models.ForeignKey(Location, blank=True, null=True)
    member_place = models.ForeignKey("Member", blank=True, null=True)
    category = models.CharField(max_length = 20)
    date = models.DateField()

    # Managers
    objects = models.Manager()
    past = PastInklingManager()
    current = CurrentInklingManager()
    
    # Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        """String representation for the current inkling."""
        if self.location is not None:
            return "%s (%s, %s)" % (self.location.name, self.date, self.category)
        else:
            return "%s (%s, %s)" % (self.member_place.first_name + " " + self.member_place.last_name + "'s Place", self.date, self.category)          

    def get_formatted_date(self, year = True, weekday = False):
        """Returns the current inkling's formatted date."""
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        if (weekday):
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            if (year):
                return "%s, %s %d, %d" % (days[self.date.weekday()], months[self.date.month - 1], self.date.day, self.date.year)
            else:
                return "%s, %s %d" % (days[self.date.weekday()], months[self.date.month - 1], self.date.day)
        else:
            if (year):
                return "%s %d, %d" % (months[self.date.month - 1], self.date.day, self.date.year)
            else:
                return "%s %d" % (months[self.date.month - 1], self.date.day)

    def get_date_url(self):
        """Returns the current inkling's date for use in a url."""
        return "%s_%s_%s/" % (self.date.month, self.date.day, self.date.year)

    def get_formatted_category(self):
        """Returns the current member's formatted category."""
        if (self.category == "dinner"):
            return "Dinner"
        elif (self.category == "pregame"):
            return "Pregame"
        elif (self.category == "mainEvent"):
            return "Main Event"
    
    def is_location_inkling(self):
        """Returns true if the inkling is for a loaction"""
        return bool(self.location)
    
    def is_member_place_inkling(self):
       """Returns true if the inkling is for a member place"""
       return bool(self.member_place)


class PastInvitationManager(models.Manager):
    """Manager which returns past invitation objects."""
    def get_query_set(self):
        return Invitation.objects.filter(inkling__date__lt = datetime.date.today())


class CurrentInvitationManager(models.Manager):
    """Manager which returns current invitation objects."""
    def get_query_set(self):
        return Invitation.objects.filter(inkling__date__gte = datetime.date.today())


class Invitation(models.Model):
    """Invitation class definition."""
    description = models.CharField(max_length = 200, default = "")
    inkling = models.ForeignKey(Inkling)
    from_member = models.ForeignKey("Member")

    # Managers
    objects = models.Manager()
    past = PastInvitationManager()
    current = CurrentInvitationManager()
    
    def __unicode__(self):
        """String representation for the current invitation."""
        return "%s - %s (%s)" % (self.inkling, self.from_member, self.description)


class ActiveMemberManager(models.Manager):
    """Manager which returns active member objects."""
    def get_query_set(self):
        return Member.objects.filter(is_active = True)


class Member(User):
    """Member class definition. Inherits from built-in Django User class."""
    blots = models.ManyToManyField(Blot)
    networks = models.ManyToManyField(Network)
    inklings = models.ManyToManyField(Inkling)

    # Member lists
    pending = models.ManyToManyField("self", symmetrical = False, related_name = "pending_related")
    accepted = models.ManyToManyField("self", symmetrical = False, related_name = "accepted_related")
    requested = models.ManyToManyField("self", symmetrical = False, related_name = "requested_related")
    followers = models.ManyToManyField("self", symmetrical = False, related_name = "followers_related")
    following = models.ManyToManyField("self", symmetrical = False, related_name = "following_related")
    
    # Profile information
    gender = models.CharField(max_length = 6)
    birthday = models.DateField()
    phone = models.CharField(max_length = 10, default = "")
    street = models.CharField(max_length = 100, default = "")
    city = models.CharField(max_length = 50, default = "")
    state = models.CharField(max_length = 2, default = "")
    zip_code = models.CharField(max_length = 5, default = "")

    # Inviations
    invitations = models.ManyToManyField(Invitation)

    # Email verification
    verification_hash = models.CharField(max_length = 32)
    verified = models.BooleanField(default = False)

    # Privacy settings
    name_privacy = models.IntegerField(max_length = 1, default = 0)
    image_privacy = models.IntegerField(max_length = 1, default = 0)
    email_privacy = models.IntegerField(max_length = 1, default = 1)
    phone_privacy = models.IntegerField(max_length = 1, default = 1)
    birthday_privacy = models.IntegerField(max_length = 1, default = 1)
    gender_privacy = models.IntegerField(max_length = 1, default = 0)
    location_privacy = models.IntegerField(max_length = 1, default = 1)
    followers_privacy = models.IntegerField(max_length = 1, default = 1)
    following_privacy = models.IntegerField(max_length = 1, default = 1)
    networks_privacy = models.IntegerField(max_length = 1, default = 1)
    inklings_privacy = models.IntegerField(max_length = 1, default = 1)
    place_privacy = models.IntegerField(max_length = 1, default = 1)
    invitations_privacy = models.IntegerField(max_length = 1, default = 1)
    
    # Email preferences
    requested_email_preference = models.BooleanField(default = True)
    accepted_email_preference = models.BooleanField(default = True)
    invited_email_preference = models.BooleanField(default = True)
    general_email_preference = models.BooleanField(default = True)
    email_format_html = models.BooleanField(default = False)

    # Managers
    objects = models.Manager()
    active = ActiveMemberManager()
    
    # Metadata
    changed_image = models.IntegerField(max_length = 3, default = 0)

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
        return "%s %s, %s" % (months[self.birthday.month - 1], self.birthday.day, self.birthday.year)

    def get_num_notifications(self):
        """Returns the current member's notification count."""
        return self.requested.count() + self.invitations.count()

    def update_verification_hash(self):
        """Updates the current member's verification hash."""
        self.verification_hash = md5(str(randint(1000, 9999))).hexdigest()

    def update_profile_information(self, first_name, last_name, phone, street, city, state, zip_code, birthday, gender):
        """Updates the current member's privacy settings."""
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.birthday = birthday
        self.gender = gender

    def update_privacy_settings(self, location, email, phone, birthday, followers, following, networks, place, inklings):
        """Updates the current member's privacy settings."""
        self.location_privacy = location
        self.email_privacy = email
        self.phone_privacy = phone
        self.birthday_privacy = birthday
        self.followers_privacy = followers
        self.following_privacy = following
        self.networks_privacy = networks
        self.place_privacy = place
        self.inklings_privacy = inklings

    def update_email_preferences(self, requested, accepted, invited, general):
        """Updates the current member's email preferences."""
        self.requested_email_preference = requested
        self.accepted_email_preference = accepted
        self.invited_email_preference = invited
        self.general_email_preference = general
