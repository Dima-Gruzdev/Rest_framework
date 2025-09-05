import re

from rest_framework.serializers import ValidationError


def validate_video_urls(value):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube\.com|youtu\.be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    if not re.match(youtube_regex, value):
        raise ValidationError(
            'Ссылка должна вести на YouTube'
            'Ссылки на другие платформы запрещены.'
        )
