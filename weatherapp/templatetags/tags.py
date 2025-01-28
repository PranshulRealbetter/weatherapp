from django import template
from datetime import datetime
from django.utils.timezone import make_aware

register = template.Library()

@register.filter
def unix(value):
    try:
        # Ensure the value is a valid number (Unix timestamp)
        timestamp = int(value)
        # Convert to a datetime object, assuming it's in UTC
        datetime_obj_with_tz = make_aware(datetime.fromtimestamp(timestamp))
        return datetime_obj_with_tz.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        # Return an empty string or a default value if conversion fails
        return "Invalid Timestamp"

register.filter('unix', unix)
