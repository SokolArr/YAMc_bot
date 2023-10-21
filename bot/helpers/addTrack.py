import requests
from helpers.getPL import get_playlist
def add_track(TOKEN: str, userId: str, parsed_link):
    userId = str(userId)
    kind = str(parsed_link['kind'])
    track_id = str(parsed_link['track_id'])
    album_id = str(parsed_link['album_id'])
    revision = str(get_playlist(TOKEN, userId, kind)['revision'])
    # print('try to add: kind, track, album',kind, track_id, album_id)
    base_api_url = 'https://api.music.yandex.net'
    req = '/users/' + userId + '/playlists/' + kind + '/change'
    diff = '[{"op": "insert", "at": 0, "tracks": [{"id":' + track_id+ ', "albumId":' + album_id+ '}]}]'
    payload = {'kind': kind, 
               'revision': revision, 
               'diff': diff}
    # print(payload)
    response = requests.post(base_api_url + req, headers = {'Authorization': 'OAuth ' + TOKEN}, data = payload).json()
    print('Added track: ', track_id, 'in kind:', kind, 'by user:', userId, 'it was ', revision, ' revision album')
    return response
    # print('\n', response) 