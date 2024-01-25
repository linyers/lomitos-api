import re
from rest_framework.serializers import ValidationError


def CustomValidations(data):
    rating_data = data.get('rating')
    if rating_data:
        RatingValidator(rating_data)

    day_time = data.get('day_time')
    night_time = data.get('night_time')
    if day_time:
        for k, v in day_time.items():
            if v:
                TimeValidator(k, v, 'day_time')

    if night_time:
        for k, v in night_time.items():
            if v:
                TimeValidator(k, v, 'night_time')

def RatingValidator(rating):
    if rating['rate']:
        if rating['rate'] > 5 or rating['rate'] < 1:
            raise ValidationError({'rate': 'Rate must be between 1 and 5'})


def TimeValidator(day, time, period):
    pattern = r'^\d{2}:\d{2}-\d{2}:\d{2}$'

    if not re.match(pattern, time):
        raise ValidationError({period: f'{day} must be respect the format 00:00-00:00'})

    start_hours, start_minutes, end_hours, end_minutes = map(int, time.replace("-", ":").split(":"))

    if not (1 <= start_hours <= 24) or not (1 <= end_hours <= 24):
        raise ValidationError({period: f'{day} hours must be between 1 and 24'})

    if not (0 <= start_minutes <= 59) or not (0 <= end_minutes <= 59):
        raise ValidationError({period: f'{period} minutes must be between 0 and 59'})