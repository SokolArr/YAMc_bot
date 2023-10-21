import requests
def create_playlist(TOKEN: str, userId: str, title: str, visibility = 'public'):
    userId = userId
    base_api_url = 'https://api.music.yandex.net'
    req = '/users/{userId}/playlists/create'
    response = requests.post(base_api_url + req, headers = {'Authorization': 'OAuth ' + TOKEN}, data = {
                                                'title': title,
                                                'visibility': visibility}).json()
    print(response) 