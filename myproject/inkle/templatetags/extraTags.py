from django import template

register = template.Library()

@register.filter(name = "truncatecharacters")
def truncatecharacters(value, arg):
    """Truncates a string after a certain number of chars. Argument: number of chars to truncate after."""
    # Get the number of chars to truncate after (or fail silently if it is not an int)
    try:
        length = int(arg)
    except ValueError:
        return value

    # Add an ellipse if applicable, otherwise, simply return the input value
    if len(value) > length:
        return value[:length] + "..."
    return value
