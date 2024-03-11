from urllib.parse import urlparse
from datetime import datetime

def dttm() -> datetime:
    return datetime.now()

def parse_link(link: str) -> list:
    try:
        album_id = urlparse(link).path.split('/')[2]
        track_id = urlparse(link).path.split('/')[4]
        return {'track_id': str(track_id), 
            'album_id': str(album_id)}
    except:
        return None
