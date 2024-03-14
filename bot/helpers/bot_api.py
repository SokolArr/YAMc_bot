import hashlib
from helpers.yam_api import *
from helpers.yam_link_parser import *

def bot_get_hash(var) -> str:
    return hashlib.shake_256(str(var).encode('utf-8')).hexdigest(5)

def bot_concat_hash_title(var: str, postfix: str) -> str:
    return str(var + postfix)

def bot_get_title_hash_all(bot, chat_id: str, chat_options) -> str:
    # Попытка сгенерировать хеш
    try:
        hash_title = bot_get_hash(chat_id)
        return bot_concat_hash_title(hash_title, '_all')
        
    # Ошибка в генерации хеша    
    except Exception as e:
        print(dttm(), chat_id, chat_options.ConsoleError.hash_gen, e)
        bot.send_message(chat_id, chat_options.ChatError.hash_gen)
        return -1
    
def bot_get_url(bot, global_options, chat_id, chat_options, playlist_title: str):
    # Получить ссылку
    try:
        playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
        
        if playlist_id != '':
            url = get_playlist_url(global_options.ya_usr_id, playlist_id)
            bot.send_message(chat_id, chat_options.Answ.get_url + url)
        else:
            raise Exception("feth no playlist")
        
    # Ошибка нет плейлиста
    except Exception as e:
        print(dttm(), chat_id, chat_options.ConsoleError.no_playlist, e)
        bot.send_message(chat_id, chat_options.ChatError.no_playlist)
        
def bot_drop_playlist(bot, global_options, chat_id, chat_options, playlist_title: str):
     # Попытка удалить плейлист
    try:
        playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
        
        if playlist_id != '':
            drop_playlist(global_options.token, global_options.ya_usr_id, playlist_id)
            bot.send_message(chat_id, chat_options.Answ.delete_playlist)
        else:
            raise Exception("feth no playlist")
        
    # Ошибка при удалении плейлиста
    except Exception as e:
        print(dttm(), chat_id, chat_options.ConsoleError.nothing_to_del, e)
        bot.send_message(chat_id, chat_options.ChatError.nothing_to_del)

def bot_create_playlist(bot, global_options, chat_id, chat_options, playlist_title: str):
    try:        
        # Если нет плейлиста
        if(if_in_playlists_by_title(global_options.token, global_options.ya_usr_id, playlist_title) == 0):
            new_playlist_id = create_playlist(global_options.token, global_options.ya_usr_id, playlist_title)
            url = get_playlist_url(global_options.ya_usr_id, new_playlist_id)
            bot.send_message(chat_id, chat_options.Answ.create_playlist + url)
            
        # Если уже есть плейлист
        else:
            playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
            url = get_playlist_url(global_options.ya_usr_id, playlist_id)
            bot.send_message(chat_id, chat_options.ChatError.already_have_playlist + url) 
    
    # Ошибка в создании плейлиста
    except Exception as e:
        print(dttm(), chat_id, chat_options.ConsoleError.create_playlist, e)
        bot.send_message(chat_id, chat_options.ChatError.create_playlist)

def bot_add_track_to_playlist(bot, global_options, chat_id, chat_options, playlist_title: str, message: str):
    try:
        # Если получается спарсить ссылку на ЯМ
        if(parse_link(message)):
            album_id = parse_link(message)['album_id']
            track_id = parse_link(message)['track_id']
            
            # Если нет плейлиста
            if(if_in_playlists_by_title(global_options.token, global_options.ya_usr_id, playlist_title) == 0):
                new_playlist_id = create_playlist(global_options.token, global_options.ya_usr_id, playlist_title)
                url = get_playlist_url(global_options.ya_usr_id, new_playlist_id)
                add_track_to_playlist(global_options.token, global_options.ya_usr_id, new_playlist_id, album_id, track_id)
                bot.send_message(chat_id, chat_options.Answ.no_playlist + url)
                
            # Если есть плейлист
            else:
                playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
                add_track_to_playlist(global_options.token, global_options.ya_usr_id, playlist_id, album_id, track_id)
                url = get_playlist_url(global_options.ya_usr_id, playlist_id)
                bot.send_message(chat_id, chat_options.Answ.add_track + url)
        
        # Неправильная ссылка
        else:
            print(dttm(), chat_id, chat_options.ConsoleError.parse_link)
            bot.send_message(chat_id, chat_options.ChatError.parse_link)
            raise Exception("bad url")
            
    # Если возникла ошибка при добавлении трека
    except Exception as e:
        print(dttm(), chat_id, chat_options.ConsoleError.add_track, e)
        bot.send_message(chat_id, chat_options.ChatError.add_track)