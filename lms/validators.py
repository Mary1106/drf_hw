from rest_framework.serializers import ValidationError
import re


def validate_links(value):
    value_list = value.split()
    pattern_for_all_links = r'(https?:\/\/|ftps?:\/\/|www\.)|(\.[a-zа-я]{2,3}\b)'
    links_regex = re.compile(pattern_for_all_links, re.IGNORECASE)
    # Находим все ссылки в поле
    link_list = []
    for item in value_list:
        if links_regex.findall(item):
            link_list.append(item)
    # Находим не-youtube ссылки
    youtube_regex = re.compile(r'youtube\.', re.IGNORECASE)
    for link in link_list:
        if not youtube_regex.findall(link):
            raise ValidationError('Вы можете размещать ссылки только на Youtube.')
