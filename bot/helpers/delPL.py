import requests
def del_playlist(TOKEN: str, userId: str, kind: str):
    userId = str(userId)
    kind = str(kind)
    # print (userId, kind)
    base_api_url = 'https://api.music.yandex.net'
    response = requests.post(base_api_url+'/users/'+userId+'/playlists/'+kind+'/delete', headers = {'Authorization': 'OAuth ' + TOKEN}).json()
    print(response)