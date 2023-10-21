from urllib.parse import urlparse
def parse_link(link: str, char_deli: str):
    track_id = 1
    album_id = 1
    linked = str(link).split(char_deli)[0]
    kind = str(link).split(char_deli)[1]
    album_id = urlparse(linked).path.split('/')[2]
    track_id = urlparse(linked).path.split('/')[4]
    return {'track_id': track_id, 'album_id': album_id, 'kind': kind}