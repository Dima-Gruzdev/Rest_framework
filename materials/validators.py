import re

from rest_framework.serializers import ValidationError


def validate_video_urls(value):
    """Класс валидации проверки видео материала"""
    if not value:
        return
    youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+\?v=([^&]+)|youtu\.be/([^&?]+)'
    if not re.match(youtube_regex, value.strip()):
        raise ValidationError('Только ссылки на YouTube.')
