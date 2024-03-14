import telebot
from telebot import types
from helpers.yam_api import *
from helpers.yam_link_parser import *
import hashlib
import time

from options import *

bot = telebot.TeleBot(TG_KEY)

@bot.message_handler(commands=['start'], chat_types=['supergroup'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        bot.send_message(chat_id, "👋 Привет! Я могу сделать общий плейлист в Яндекс Музыке!\n Чтобы узнать как введи /help")
        
@bot.message_handler(commands=['start'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.from_user.id
        bot.send_message(chat_id, "👋 Привет! Я могу сделать общий плейлист в Яндекс Музыке!\n Чтобы узнать как введи /help") 
    
@bot.message_handler(commands=['help'], chat_types=['supergroup'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        bot.send_message(chat_id, "Чтобы обратиться ко мне в беседе начни фразу с @YAMc_bot, а потом отправь ссылку на трек\nНапример: @YAMc_bot https://music.yandex.ru/album/29998108/track/123237014")
        bot.send_message(chat_id, "Я понимаю команды:\n_дай ссылку_ - вернет ссылку на плейлист\n_удали плейлист_ - удалит плейлист\n_создай плейлист_ - создаст плейлист", parse_mode= 'Markdown')
@bot.message_handler(commands=['help'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.from_user.id
        bot.send_message(chat_id, "Отправь мне ссылку на трек в формате\nhttps://music.yandex.ru/album/29998108/track/123237014")
        bot.send_message(chat_id, "Я понимаю команды:\n_дай ссылку_ - вернет ссылку на плейлист\n_удали плейлист_ - удалит плейлист\n_создай плейлист_ - создаст плейлист", parse_mode= 'Markdown')

@bot.message_handler(chat_types=['private'])
def get_text_messages(message):
    if message.date > bot_time_start:
        mes_txt = message.text
        tg_usr_id = message.from_user.id
        
        try:
            sha_tg_usr_id = hashlib.shake_256(str(tg_usr_id).encode('utf-8')).hexdigest(5)
            playlist_title = str(sha_tg_usr_id + '_all')
        except:
            bot.send_message(tg_usr_id, "Ошибка в генерации хеша")  
            print(dttm(), tg_usr_id, ' - ERROR to get hash')
            return
        
        if(mes_txt.lower().find('дай ссылку') >= 0):
            try:
                url = get_playlist_url(YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title))
                bot.send_message(tg_usr_id, "Держи\n" + url)
            except:
                bot.send_message(tg_usr_id, "Не нашел твой плейлист! Попробуй создать его,\nпопроси добавить трек:\nВведи /help для помощи")
        elif(mes_txt.lower().find('удали плейлист') >= 0):
            try:
                drop_playlist(TOKEN, YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title))
                bot.send_message(tg_usr_id, "Удалил!\n")
            except:
                bot.send_message(tg_usr_id, "Нечего удалять! Сначала надо его создать,\nпопроси добавить трек:\nВведи /help для помощи")
        elif(mes_txt.lower().find('создай плейлист') >= 0):
            try:
                if(if_in_playlists_by_title(TOKEN, YA_USR_ID, playlist_title) == 0):
                    new_playlist_id = create_playlist(TOKEN, YA_USR_ID, playlist_title)
                    url = get_playlist_url(YA_USR_ID, new_playlist_id)
                    bot.send_message(tg_usr_id, "Создал плейлист!\n" + url)
                else:
                    url = get_playlist_url(YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title))
                    bot.send_message(tg_usr_id, "Плейлист уже создан!\n" + url) 
            except:
                bot.send_message(tg_usr_id, "Ошибка в создании плейлиста")
                print(dttm(), tg_usr_id, ' - ERROR to create playlist')
        elif(mes_txt.lower().find('https') >= 0):
            try:
                if(parse_link(mes_txt)):
                    album_id = parse_link(mes_txt)['album_id']
                    track_id = parse_link(mes_txt)['track_id']
                    
                    sha_tg_usr_id = hashlib.shake_256(str(tg_usr_id).encode('utf-8')).hexdigest(5)
                    playlist_title = str(sha_tg_usr_id + '_all')
                    
                    if(if_in_playlists_by_title(TOKEN, YA_USR_ID, playlist_title) == 0):
                        new_playlist_id = create_playlist(TOKEN, YA_USR_ID, playlist_title)
                        url = get_playlist_url(YA_USR_ID, new_playlist_id)
                        
                        add_track_to_playlist(TOKEN, YA_USR_ID, new_playlist_id, album_id, track_id)
                        bot.send_message(tg_usr_id, "У тебя не было общего плейлиста, я создал его и закинул туда трек\n" + url)
                    else:
                        playlist_id = get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title)
                        
                        add_track_to_playlist(TOKEN, YA_USR_ID, playlist_id, album_id, track_id)
                        bot.send_message(tg_usr_id, "Закинул трек в плейлист\n" + get_playlist_url(YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title)))
                else:
                    print(dttm(), tg_usr_id, '- ERROR parse link')
                    bot.send_message(tg_usr_id, "Не могу спарсить ссылку, проверь корректность\n")  
            except:
                print(dttm(), tg_usr_id, '- ERROR add track')
        
@bot.message_handler(content_types=['text'], chat_types=['supergroup'])
def get_text_messages(message):
    if message.text[0:9] == '@YAMc_bot' and message.date > bot_time_start:
        mes_txt = message.text[10:]
        tg_usr_id = message.chat.id

        try:
            sha_tg_usr_id = hashlib.shake_256(str(tg_usr_id).encode('utf-8')).hexdigest(5)
            playlist_title = str(sha_tg_usr_id + '_all')
        except:
            bot.send_message(tg_usr_id, "Ошибка в генерации хеша")  
            print(dttm(), tg_usr_id, ' - ERROR to get hash')
            return
        
        if(mes_txt.lower().find('дай ссылку') >= 0):
            try:
                url = get_playlist_url(YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title))
                bot.send_message(tg_usr_id, "Держи\n" + url)
            except:
                bot.send_message(tg_usr_id, "Не нашел твой плейлист! Попробуй создать его,\nпопроси добавить трек:\nВведи /help для помощи")
        elif(mes_txt.lower().find('удали плейлист') >= 0):
            try:
                drop_playlist(TOKEN, YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title))
                bot.send_message(tg_usr_id, "Удалил!\n")
            except:
                bot.send_message(tg_usr_id, "Нечего удалять! Сначала надо его создать,\nпопроси добавить трек:\nВведи /help для помощи")
        elif(mes_txt.lower().find('создай плейлист') >= 0):
            try:
                if(if_in_playlists_by_title(TOKEN, YA_USR_ID, playlist_title) == 0):
                    new_playlist_id = create_playlist(TOKEN, YA_USR_ID, playlist_title)
                    url = get_playlist_url(YA_USR_ID, new_playlist_id)
                    bot.send_message(tg_usr_id, "Создал плейлист!\n" + url)
                else:
                    url = get_playlist_url(YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title))
                    bot.send_message(tg_usr_id, "Плейлист уже создан!\n" + url) 
            except:
                bot.send_message(tg_usr_id, "Ошибка в создании плейлиста")
                print(dttm(), tg_usr_id, ' - ERROR to create playlist')
        elif(mes_txt.lower().find('https') >= 0):
            try:
                if(parse_link(mes_txt)):
                    album_id = parse_link(mes_txt)['album_id']
                    track_id = parse_link(mes_txt)['track_id']
                    
                    sha_tg_usr_id = hashlib.shake_256(str(tg_usr_id).encode('utf-8')).hexdigest(5)
                    playlist_title = str(sha_tg_usr_id + '_all')
                    
                    if(if_in_playlists_by_title(TOKEN, YA_USR_ID, playlist_title) == 0):
                        new_playlist_id = create_playlist(TOKEN, YA_USR_ID, playlist_title)
                        url = get_playlist_url(YA_USR_ID, new_playlist_id)
                        
                        add_track_to_playlist(TOKEN, YA_USR_ID, new_playlist_id, album_id, track_id)
                        bot.send_message(tg_usr_id, "Не было общего плейлиста, я создал его и закинул туда трек\n" + url)
                    else:
                        playlist_id = get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title)
                        
                        add_track_to_playlist(TOKEN, YA_USR_ID, playlist_id, album_id, track_id)
                        bot.send_message(tg_usr_id, "Закинул трек в плейлист\n" + get_playlist_url(YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title)))
                else:
                    print(dttm(), tg_usr_id, '- ERROR parse link')
                    bot.send_message(tg_usr_id, "Не могу спарсить ссылку, проверь корректность\n")  
            except:
                print(dttm(), tg_usr_id, '- ERROR add track')
        

if __name__ == "__main__":
    try:
        print(dttm(), 'BOT STARTED','\n')
        bot_time_start = time.mktime(datetime.now().timetuple())
        if(TG_ADMIN_ID != ''):bot.send_message(TG_ADMIN_ID, 'Я ожил!')
        bot.polling()
    except Exception as e:
        if(TG_ADMIN_ID != ''):bot.send_message(TG_ADMIN_ID, 'Я прилег! ' + str(e))
        print(dttm(), 'BOT DOWN','\n')
        print(dttm(), e)