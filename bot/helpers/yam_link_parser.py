from urllib.parse import urlparse
from datetime import datetime
import re

def dttm() -> str:
    return  str(datetime.now()) + ' | '

def parse_link(link: str) -> list:
    try:
        cat_link = re.search("(?P<url>https?://music.yandex.ru[^\s]+)", link).group("url")
        album_id = int(urlparse(cat_link).path.split('/')[2])
        track_id = int(urlparse(cat_link).path.split('/')[4])
        return {'track_id': str(track_id), 
                'album_id': str(album_id)}
    except:
        return None