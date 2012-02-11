from django import template
from django.template.defaultfilters import stringfilter

# Date object
from datetime import date

# Choices for months, states, and location categories
from myproject.inkle.choices import *
from myproject.settings import DEBUG

register = template.Library()

@register.filter()
@stringfilter
def truncate_characters(value, arg):
    """Truncates a string after a certain number of characters."""
    # Get the number of chars to truncate after (or fail silently if it is not an int)
    try:
        length = int(arg)
    except ValueError:
        return value

    # Add an ellipse if applicable, otherwise, simply return the input value
    if len(value) > length:
        return "%s..." % value[0:(length - 3)]
    return value
truncate_characters.is_safe = True

@register.filter()
@stringfilter
def split(value):
    """Splits a string at the whitespace."""
    return value.split()
split.is_safe = True

@register.filter()
def days(value, arg):
    """Returns a range object for the birthday day select."""
    # Get the specified month and year (or set them both to 0)
    try:
        month = int(value)
    except ValueError:
        month = 0
    try:
        year = int(arg)
    except ValueError:
        year = 0

    # February
    if (month == 2):
        # Non-leap year
        if (year % 4 != 0):
            return range(1, 29)
        
        # Leap year or no year specified (i.e. year = 0)
        else:
            return range(1, 30)

    # April, June, September, and November
    elif month in [4, 6, 9, 11]:
        return range(1, 31)

    # January, March, May, July, August, October, and December
    else:
        return range(1, 32)
days.is_safe = True


@register.filter()
def months(value):
    """Returns a list of the months and their abbreviations."""
    return MONTHS
months.is_safe = True

@register.filter()
def years(value):
    """Returns a range object for the birthday year select."""
    # Get the number of years for the year range (or set it to 100 by default)
    try:
        num_years = int(value)
    except ValueError:
        num_years = 100

    # Get today's date object
    today = date.today()

    # Return the reversed date range
    return reversed(range((today.year - num_years), (today.year + 1)))
years.is_safe = True


@register.filter()
def states(value):
    """Returns a list of the states and their abbreviations."""
    return STATES
states.is_safe = True


@register.filter()
def location_categories(value):
    """Returns a list of the location categories."""
    return LOCATION_CATEGORIES
location_categories.is_safe = True


@register.filter()
def debug_value(value):
    """Returns the value of DEBUG."""
    return DEBUG
debug_value.is_safe = True


@register.filter()
def clean_url(value):
    """Returns the website's URL without the http://www. portion."""
    if value.endswith("/"):
        value = value[:-1]
    if ((value.startswith("http://www.")) or (value.startswith("https://www.")) or (value.startswith("www."))):
        return value.split("www.")[1]
    elif ((value.startswith("http://")) or (value.startswith("https://"))):
        return value.split("://")[1]
    else:
        return value
debug_value.is_safe = True
