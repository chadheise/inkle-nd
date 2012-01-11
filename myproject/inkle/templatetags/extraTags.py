from django import template
from datetime import date

register = template.Library()

@register.filter(name = "truncate_characters")
def truncate_characters(value, arg):
    """Truncates a string after a certain number of characters."""
    # Get the number of chars to truncate after (or fail silently if it is not an int)
    try:
        length = int(arg)
    except ValueError:
        return value

    # Add an ellipse if applicable, otherwise, simply return the input value
    if len(value) > length:
        return value[:(length - 3)] + "..."
    return value

@register.filter(name = "split")
def split(value):
    """Splits a string at the whitespace."""
    return value.split()

@register.filter(name = "day_range")
def day_range(value):
    """Returns a range object with values 1 to 31 (for the birthday day select)."""
    return range(1, 32)

@register.filter(name = "year_range")
def day_range(value):
    """Returns a range object with values 1900 to the current year (for the birthday year select)."""
    return reversed(range(1900, (date.today().year + 1)))
