from django.core.exceptions import ValidationError

def size_checker(value):
    limit = 1000000
    if value.size > limit:
        raise ValidationError('Image size is greater than 1mb')
