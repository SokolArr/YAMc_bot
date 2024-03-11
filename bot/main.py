import telebot
from telebot import types
from helpers.yam_api import *
from helpers.yam_link_parser import *
import hashlib
import time

from options import *

bot = telebot.TeleBot(TG_KEY)

print(dttm(), 'BOT STARTED','\n')
bot_time_start = time.mktime(dttm().timetuple())

@bot.message_handler(commands=['start'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.from_user.id
        print(dttm(), 'User', chat_id, 'start talk with bot','\n')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/start")
        
        markup.add(btn1)
        bot.send_message(chat_id, "👋 Привет! Я тут за музыку Яндекса шарю!\n Чтобы узнать комманды введи /help") 
    
@bot.message_handler(commands=['help'], chat_types=['supergroup'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        print(dttm(), 'User', chat_id, 'start talk with bot','\n')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/help")
        
        markup.add(btn1)
        bot.send_message(chat_id, "Чтобы обратиться ко мне в беседе начни фразу с @YAMc_bot, а потом отправь ссылку на трек\nНапример: @YAMc_bot https://music.yandex.ru/album/29998108/track/123237014")

@bot.message_handler(commands=['help'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.from_user.id
        print(dttm(), 'User', chat_id, 'start talk with bot','\n')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/help")
        
        markup.add(btn1)
        bot.send_message(chat_id, "Отправь мне ссылку на трек в формате\n https://music.yandex.ru/album/29998108/track/123237014")

@bot.message_handler(chat_types=['private'])
def get_text_messages(message):
    if message.date > bot_time_start:
        mes_txt = message.text
        tg_usr_id = message.from_user.id
        
        print(dttm(), tg_usr_id, mes_txt)
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
                    print(dttm(), tg_usr_id, '|', sha_tg_usr_id, 'add new track', track_id, 'from album', album_id, 'in playlist', new_playlist_id)
                    
                    bot.send_message(tg_usr_id, "У тебя не было общего плейлиста, я создал его и закинул туда трек\n" + url)
                else:
                    playlist_id = get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title)
                    
                    add_track_to_playlist(TOKEN, YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title), album_id, track_id)
                    print(dttm(), tg_usr_id, '|', sha_tg_usr_id, 'add new track', track_id, 'from album', album_id, 'in playlist', playlist_id)
                    
                    bot.send_message(tg_usr_id, "Закинул трек в плейлист\n" + get_playlist_url(YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title)))
            else:
                print(dttm(), tg_usr_id, 'bad link')
                bot.send_message(tg_usr_id, "Не могу спарсить ссылку, проверь корректность\n")  
        except:
            print(dttm(), 'ERROR add track by usr:', tg_usr_id)
        
@bot.message_handler(content_types=['text'], chat_types=['supergroup'])
def get_text_messages(message):
    if message.text[0:9] == '@YAMc_bot' and message.date > bot_time_start:
        mes_txt = message.text[10:]
        tg_usr_id = message.chat.id
        
        print(dttm(), tg_usr_id, mes_txt)
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
                    print(dttm(), tg_usr_id, '|', sha_tg_usr_id, 'add new track', track_id, 'from album', album_id, 'in playlist', new_playlist_id)
                    
                    bot.send_message(tg_usr_id, "Не было общего плейлиста, я создал его и закинул туда трек\n" + url)
                else:
                    playlist_id = get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title)
                    
                    add_track_to_playlist(TOKEN, YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title), album_id, track_id)
                    print(dttm(), tg_usr_id, '|', sha_tg_usr_id, 'add new track', track_id, 'from album', album_id, 'in playlist', playlist_id)
                    
                    bot.send_message(tg_usr_id, "Закинул трек в плейлист\n" + get_playlist_url(YA_USR_ID, get_playlist_id_by_title(TOKEN, YA_USR_ID, playlist_title)))
            else:
                print(dttm(), tg_usr_id, 'bad link')
                bot.send_message(tg_usr_id, "Не могу спарсить ссылку, проверь корректность\n")  
        except:
            print(dttm(), 'ERROR add track by usr:', tg_usr_id)
        
    
bot.polling()
print(dttm(), 'BOT DOWN','\n')