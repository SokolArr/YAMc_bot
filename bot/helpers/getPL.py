import requests
def get_playlists(TOKEN: str, userId: str):
    userId = userId
    req = '/users/{userId}/playlists/list'
    base_api_url = 'https://api.music.yandex.net'
    playlist_titles = []
    # print(base_api_url + req)
    response = requests.get(base_api_url + req, headers = {'Authorization': 'OAuth ' + TOKEN}).json()['result']
    # print(response)
    for idx in range(0, len(response)):
        playlist_titles.append({'kind': response[idx]['kind'], 'revision': response[idx]['revision'],'title': response[idx]['customWave']['title']})
    return playlist_titles

def get_playlist(TOKEN: str, userId: str, kind: str):
    userId = userId
    req = '/users/{userId}/playlists/list'
    base_api_url = 'https://api.music.yandex.net'
    response = requests.get(base_api_url + req, headers = {'Authorization': 'OAuth ' + TOKEN}).json()['result']
    for idx in range(0, len(response)):
        if str(response[idx]['kind']) == str(kind):
           return {'kind': response[idx]['kind'], 'revision': response[idx]['revision'],'title': response[idx]['customWave']['title']}
        else: return 'no such playlist'
        
def get_uid_playlist(TOKEN: str, kind: str):
    try:
        req = '/users/{userId}/playlists/list'
        base_api_url = 'https://api.music.yandex.net'
        response = requests.get(base_api_url + req, headers = {'Authorization': 'OAuth ' + TOKEN}).json()['result']
        for idx in range(0, len(response)):
            if str(response[idx]['kind']) == str(kind):
                return str(response[idx]['uid'])
            else: return 'no such playlist'
    except:
        return -1