from helpers.yam_link_parser    import *
from helpers.utils.bot_logger   import *
import requests

# Создать плейлист
def create_playlist(token: str, ya_usr_id: str, title: str, visibility = 'public') -> str:
    base_api_url = 'https://api.music.yandex.net'
    req = '/users/'+ ya_usr_id + '/playlists/create'
    try:
        response = requests.post(base_api_url + req, 
                                 headers = {'Authorization': 'OAuth ' + token}, 
                                 data    = {'title': title,
                                            'visibility': visibility}
                                ).json()
        playlist_title = response['result']['title']
        playlist_id = response['result']['kind']
        if response['result']:
            print(dttm(), ya_usr_id, 'created playlist', playlist_id, '"' + playlist_title + '"')
            return str(response['result']['kind'])
        else:
            print(dttm(), 'ERROR no response')
            return -1
    except:
        print(dttm(), 'ERROR no response')
        return -1
    
    
# Удалить плейлист
def drop_playlist(token: str, ya_usr_id: str, playlist_id: str) -> str:
    base_api_url = 'https://api.music.yandex.net'
    req = '/users/' + ya_usr_id + '/playlists/' + playlist_id + '/delete'
    try:
        response = requests.post(base_api_url + req, 
                                 headers = {'Authorization': 'OAuth ' + token}
                                ).json()
        result = response['result']
        if result:
            print(dttm(), ya_usr_id, 'delete playlist', playlist_id)
            return playlist_id
        else:
            print(dttm(), 'ERROR no response')
            return -1
    except:
        print(dttm(), 'ERROR no response')
        return -1

# Получить плейлисты
def get_playlists(token: str, ya_usr_id: str) -> list:
    base_api_url = 'https://api.music.yandex.net'
    req = '/users/' + ya_usr_id + '/playlists/' + '/list'
    result_array = []
    try:
        response = requests.get(base_api_url + req,
                                headers = {'Authorization': 'OAuth ' + token}
                            ).json()
        result = response['result']
        if result:
            for i in range(len(result)):
                playlist = {
                    'playlist_id' : str(result[i]['kind']),
                    'title'       : str(result[i]['title']),
                    'visibility'  : str(result[i]['visibility']),
                    'revision'    : str(result[i]['revision'])
                }
                result_array.append(playlist)
            return result_array
        else:
            return -1
    except:
        print(dttm(), 'ERROR no response')
        return -1
    
# Если существует плейлист
def if_in_playlists(token: str, ya_usr_id: str, playlist_id: str) -> int:
    playlists = get_playlists(token, ya_usr_id)
    for i in range(len(playlists)):
        if(playlists[i]['playlist_id'] == playlist_id):
            return 1
    return 0

# Если существует плейлист
def if_in_playlists_by_title(token: str, ya_usr_id: str, title: str) -> int:
    playlists = get_playlists(token, ya_usr_id)
    for i in range(len(playlists)):
        if(playlists[i]['title'] == title):
            return 1
    return 0

# Получить плейлист
def get_playlist(token: str, ya_usr_id: str, playlist_id: str) -> list:
    playlists = get_playlists(token, ya_usr_id)
    for i in range(len(playlists)):
        if(playlists[i]['playlist_id'] == playlist_id):
            return playlists[i]
    return -1

# Получить плейлист
def get_playlist_id_by_title(token: str, ya_usr_id: str, title: str) -> str:
    playlists = get_playlists(token, ya_usr_id)
    for i in range(len(playlists)):
        if(playlists[i]['title'] == title):
            return playlists[i]['playlist_id']
    return ''
    
# Получить ревизию плейлиста
def get_revision_of_playlist(token: str, ya_usr_id: str, playlist_id: str) -> int:
    return int(get_playlist(token, ya_usr_id, playlist_id)['revision'])

# Добавить трек в плейлист
def add_track_to_playlist(token: str, ya_usr_id: str, playlist_id: str, album_id: str, track_id: str) -> int:
    revision = get_revision_of_playlist(token, ya_usr_id, playlist_id)
    base_api_url = 'https://api.music.yandex.net'
    req = '/users/' + ya_usr_id + '/playlists/' + playlist_id + '/change'
    diff = '[{"op": "insert", "at": 0, "tracks": [{"id":' + track_id + ', "albumId":' + album_id + '}]}]'
    payload = {'kind': playlist_id, 
               'revision': revision, 
               'diff': diff
              }
    try:
        response = requests.post(base_api_url + req, 
                                headers = {'Authorization': 'OAuth ' + token}, 
                                data = payload
                                ).json()
        if(response):
            print(dttm(), ya_usr_id, 'add new track', track_id, 'from album', album_id, 'in playlist', playlist_id)
            return 1
    except:
        print(dttm(), 'ERROR no response')
        return -1
    
# Удалить трек из плейлиста
def delete_track_from_playlist(token: str, ya_usr_id: str, playlist_id: str, album_id: str, track_id: str) -> int:
    revision = get_revision_of_playlist(token, ya_usr_id, playlist_id)
    base_api_url = 'https://api.music.yandex.net'
    req = '/users/' + ya_usr_id + '/playlists/' + playlist_id + '/change'
    diff = '[{"op": "delete", "from":0, "to":1, "tracks": [{"id":' + track_id + ', "albumId":' + album_id + '}]}]'
    
    payload = {'kind': playlist_id, 
               'revision': revision, 
               'diff': diff
              }
    try:
        response = requests.post(base_api_url + req, 
                                headers = {'Authorization': 'OAuth ' + token}, 
                                data = payload
                                ).json()
        if(response):
            print(dttm(), ya_usr_id, 'delete track', track_id, 'from album', album_id, 'in playlist', playlist_id)
            return 1
    except:
        print(dttm(), 'ERROR no response')
        return -1
    
def get_playlist_url(ya_usr_id: str, playlist_id: str) -> str:
        return 'https://music.yandex.ru/users/'+ ya_usr_id + '/playlists/' + playlist_id
    
