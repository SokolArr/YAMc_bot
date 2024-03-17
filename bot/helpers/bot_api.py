from helpers.yam_api                    import *
from helpers.utils.yam_link_parser      import *
from helpers.utils.bot_logger           import *
import hashlib

def bot_get_hash(var, len = 5) -> str:
    return hashlib.shake_256(str(var).encode('utf-8')).hexdigest(len)

def bot_concat_hash_title(var: str, postfix: str) -> str:
    return str(var + postfix)
        
# Для супергрупп
def bot_get_title_hash_all_for_supergroup(bot, chat_id, thread_id, chat_options) -> str:
    # Попытка сгенерировать хеш
    try:
        if(thread_id):
            hash_chat_id = bot_get_hash(chat_id)
            hash_thread_id = bot_get_hash(thread_id, 3)
            return bot_concat_hash_title(hash_chat_id + '_' + hash_thread_id, ' _t')
        else:
            if(int(chat_id) > 0):
                hash_chat_id = bot_get_hash(chat_id)
                return bot_concat_hash_title(hash_chat_id, '_p')
            else:
                hash_chat_id = bot_get_hash(chat_id)
                return bot_concat_hash_title(hash_chat_id, '_g')
        
    # Ошибка в генерации хеша    
    except Exception as e:
        write_log(chat_options.ConsoleError.hash_gen, chat_id=chat_id, thread_id=thread_id, exception=e)
        bot.send_message(chat_id, chat_options.ChatError.hash_gen, message_thread_id = thread_id)
        return -1
    
def bot_get_url_for_supergroup(bot, global_options, chat_id, thread_id, chat_options, playlist_title: str):
    # Получить ссылку
    try:
        playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
        
        if playlist_id != '':
            url = get_playlist_url(global_options.ya_usr_id, playlist_id)
            bot.send_message(chat_id, chat_options.Answ.get_url + url, message_thread_id = thread_id)
            write_log('get url: ' + url, global_options, chat_id, thread_id)
        else:
            write_log(chat_options.ConsoleError.no_playlist, global_options, chat_id, thread_id, state='Warn')
            bot.send_message(chat_id, chat_options.ChatError.no_playlist, message_thread_id = thread_id)
    
    # Ошибка при получении ссылки
    except Exception as e:
        write_log(chat_options.ConsoleError.get_url, chat_id=chat_id, thread_id=thread_id, exception=e)
        bot.send_message(chat_id, chat_options.ChatError.get_url, message_thread_id = thread_id)
        
def bot_drop_playlist_for_supergroup(bot, global_options, chat_id, thread_id, chat_options, playlist_title: str):
    # Попытка удалить плейлист
    try:
        playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
        
        if playlist_id != '':
            drop_playlist(global_options.token, global_options.ya_usr_id, playlist_id)
            bot.send_message(chat_id, chat_options.Answ.delete_playlist, message_thread_id = thread_id)
            write_log('drop playlist', global_options, chat_id, thread_id)
        else:
            write_log("feth no playlist", global_options, chat_id, thread_id, state='Warn')
            bot.send_message(chat_id, chat_options.ChatError.nothing_to_del, message_thread_id = thread_id)
                    
    # Ошибка при удалении плейлиста
    except Exception as e:
        write_log(chat_options.ConsoleError.drop_playlist, chat_id=chat_id, thread_id=thread_id, exception=e)
        bot.send_message(chat_id, chat_options.ChatError.drop_playlist, message_thread_id = thread_id)

def bot_create_playlist_for_supergroup(bot, global_options, chat_id, thread_id, chat_options, playlist_title: str):
    try:        
        # Если нет плейлиста
        if(if_in_playlists_by_title(global_options.token, global_options.ya_usr_id, playlist_title) == 0):
            new_playlist_id = create_playlist(global_options.token, global_options.ya_usr_id, playlist_title)
            url = get_playlist_url(global_options.ya_usr_id, new_playlist_id)
            bot.send_message(chat_id, chat_options.Answ.create_playlist + url, message_thread_id = thread_id)
            write_log('add playlist: ' + url, global_options, chat_id, thread_id)
            
        # Если уже есть плейлист
        else:
            playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
            url = get_playlist_url(global_options.ya_usr_id, playlist_id)
            bot.send_message(chat_id, chat_options.ChatError.already_have_playlist + url, message_thread_id = thread_id)
            write_log('already_have_playlist: ' + url, global_options, chat_id, thread_id, state='Warn')
    
    # Ошибка в создании плейлиста
    except Exception as e:
        write_log(chat_options.ConsoleError.create_playlist, chat_id=chat_id, thread_id=thread_id, exception=e)
        bot.send_message(chat_id, chat_options.ChatError.create_playlist, message_thread_id = thread_id)
        
def bot_add_track_to_playlist_for_supergroup(bot, global_options, chat_id, thread_id, chat_options, playlist_title: str, message: str):
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
                bot.send_message(chat_id, chat_options.Answ.no_playlist + url, message_thread_id = thread_id)
                write_log('create playlist: ' + url, global_options, chat_id, thread_id)
                
            # Если есть плейлист
            else:
                playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
                add_track_to_playlist(global_options.token, global_options.ya_usr_id, playlist_id, album_id, track_id)
                url = get_playlist_url(global_options.ya_usr_id, playlist_id)
                bot.send_message(chat_id, chat_options.Answ.add_track + url, message_thread_id = thread_id)
                write_log('add track: ' + url, global_options, chat_id, thread_id)
        
        # Неправильная ссылка
        else:
            write_log(chat_options.ConsoleError.parse_link, chat_id=chat_id, thread_id=thread_id, state='Warn')
            bot.send_message(chat_id, chat_options.ChatError.parse_link, message_thread_id = thread_id)
            raise Exception("bad url")
            
    # Если возникла ошибка при добавлении трека
    except Exception as e:
        write_log(chat_options.ConsoleError.add_track, chat_id=chat_id, thread_id=thread_id, exception=e)
        bot.send_message(chat_id, chat_options.ChatError.add_track, message_thread_id = thread_id)
        
        
# Для чатов и групп
def bot_get_title_hash_all(bot, chat_id: str, chat_options) -> str:
    # Попытка сгенерировать хеш
    try:
        if(int(chat_id) > 0):
            hash_chat_id = bot_get_hash(chat_id)
            return bot_concat_hash_title(hash_chat_id, '_p')
        else:
            hash_chat_id = bot_get_hash(chat_id)
            return bot_concat_hash_title(hash_chat_id, '_g')
        
    # Ошибка в генерации хеша    
    except Exception as e:
        write_log(chat_options.ConsoleError.hash_gen, chat_id=chat_id, exception=e)
        bot.send_message(chat_id, chat_options.ChatError.hash_gen)
        return -1

def bot_get_url(bot, global_options, chat_id, chat_options, playlist_title: str):
    # Получить ссылку
    try:
        playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
        
        if playlist_id != '':
            url = get_playlist_url(global_options.ya_usr_id, playlist_id)
            bot.send_message(chat_id, chat_options.Answ.get_url + url)
            write_log('get url: ' + url, global_options, chat_id)
        else:
            write_log(chat_options.ConsoleError.no_playlist, chat_id=chat_id, state='Warn')
            bot.send_message(chat_id, chat_options.ChatError.no_playlist)
        
    # Ошибка нет плейлиста
    except Exception as e:
        write_log(chat_options.ConsoleError.get_url, chat_id=chat_id, exception=e)
        bot.send_message(chat_id, chat_options.ChatError.get_url)
        
def bot_drop_playlist(bot, global_options, chat_id, chat_options, playlist_title: str):
    # Попытка удалить плейлист
    try:
        playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
        
        if playlist_id != '':
            drop_playlist(global_options.token, global_options.ya_usr_id, playlist_id)
            bot.send_message(chat_id, chat_options.Answ.delete_playlist)
            write_log('drop playlist', global_options, chat_id)
        else:
            write_log("feth no playlist", global_options, chat_id, state='Warn')
            bot.send_message(chat_id, chat_options.ChatError.nothing_to_del)
                    
    # Ошибка при удалении плейлиста
    except Exception as e:
        write_log(chat_options.ConsoleError.drop_playlist, chat_id=chat_id, exception=e)
        bot.send_message(chat_id, chat_options.ChatError.drop_playlist)

def bot_create_playlist(bot, global_options, chat_id, chat_options, playlist_title: str):
    try:        
        # Если нет плейлиста
        if(if_in_playlists_by_title(global_options.token, global_options.ya_usr_id, playlist_title) == 0):
            new_playlist_id = create_playlist(global_options.token, global_options.ya_usr_id, playlist_title)
            url = get_playlist_url(global_options.ya_usr_id, new_playlist_id)
            bot.send_message(chat_id, chat_options.Answ.create_playlist + url)
            write_log('add playlist: ' + url, global_options, chat_id)
            
        # Если уже есть плейлист
        else:
            playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
            url = get_playlist_url(global_options.ya_usr_id, playlist_id)
            bot.send_message(chat_id, chat_options.ChatError.already_have_playlist + url)
            write_log('already_have_playlist: ' + url, global_options, chat_id, state='Warn')

    # Ошибка в создании плейлиста
    except Exception as e:
        write_log(chat_options.ConsoleError.create_playlist, chat_id=chat_id, exception=e)
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
                write_log('create playlist: ' + url, global_options, chat_id)
                
            # Если есть плейлист
            else:
                playlist_id = get_playlist_id_by_title(global_options.token, global_options.ya_usr_id, playlist_title)
                add_track_to_playlist(global_options.token, global_options.ya_usr_id, playlist_id, album_id, track_id)
                url = get_playlist_url(global_options.ya_usr_id, playlist_id)
                bot.send_message(chat_id, chat_options.Answ.add_track + url)
                write_log('add track: ' + url, global_options, chat_id)
        
        # Неправильная ссылка
        else:
            write_log(chat_options.ConsoleError.parse_link, chat_id=chat_id, state='Warn')
            bot.send_message(chat_id, chat_options.ChatError.parse_link)
            raise Exception("bad url")
            
    # Если возникла ошибка при добавлении трека
    except Exception as e:
        write_log(chat_options.ConsoleError.add_track, chat_id=chat_id, exception=e)
        bot.send_message(chat_id, chat_options.ChatError.add_track)