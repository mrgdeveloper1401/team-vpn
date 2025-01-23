from rest_framework.validators import ValidationError


def integer_device_number(value):
    if not isinstance(value, int):
        raise ValidationError({"device_number": "Value must be an integer."})
    return value
