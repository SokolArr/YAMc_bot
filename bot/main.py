import telebot
from helpers.yam_api import *
from helpers.yam_link_parser import *
from helpers.bot_api import *
import time

from options import *
from creds import *

g_ops = GlobalOptions(TOKEN, YA_USR_ID, TG_KEY, BOT_TAG)
p_chat_ops = PrivateChatOptions
g_chat_ops = GroupChatOptions
bot = telebot.TeleBot(g_ops.tg_key)

# Групповые чаты
@bot.message_handler(commands=['start'], chat_types=['supergroup', 'group'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        bot.send_message(chat_id, g_chat_ops.Greeting.main) 
        
@bot.message_handler(commands=['help'], chat_types=['supergroup', 'group'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        bot.send_message(chat_id, g_chat_ops.Help(g_ops.bot_tag).get_about_send(), parse_mode= 'Markdown')
        bot.send_message(chat_id, g_chat_ops.Help(g_ops.bot_tag).get_commands(), parse_mode= 'Markdown')

@bot.message_handler(commands=['create_pl'], chat_types=['supergroup', 'group'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, g_chat_ops)
        bot_create_playlist(bot, g_ops, chat_id, g_chat_ops, playlist_title)
        
@bot.message_handler(commands=['drop_pl'], chat_types=['supergroup', 'group'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, g_chat_ops)
        bot_drop_playlist(bot, g_ops, chat_id, g_chat_ops, playlist_title)

@bot.message_handler(commands=['link'], chat_types=['supergroup', 'group'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, g_chat_ops)
        bot_get_url(bot, g_ops, chat_id, g_chat_ops, playlist_title)
        
@bot.message_handler(content_types=['text'], chat_types=['supergroup', 'group'])
def get_text_messages(message):
    if message.text[0:len(g_ops.bot_tag)] == g_ops.bot_tag and message.date > bot_time_start:
        mes_txt = message.text[len(g_ops.bot_tag)+1:]
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, g_chat_ops)
        
        if(mes_txt.lower().find('дай ссылку') >= 0):
            bot_get_url(bot, g_ops, chat_id, g_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('удали плейлист') >= 0):
            bot_drop_playlist(bot, g_ops, chat_id, g_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('создай плейлист') >= 0):
            bot_create_playlist(bot, g_ops, chat_id, g_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('https') >= 0):
            bot_add_track_to_playlist(bot, g_ops, chat_id, g_chat_ops, playlist_title, mes_txt)
            
        
# Private чаты
@bot.message_handler(commands=['start'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.from_user.id
        bot.send_message(chat_id, p_chat_ops.Greeting.main) 

@bot.message_handler(commands=['help'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.from_user.id
        bot.send_message(chat_id, p_chat_ops.Help.about_send)
        bot.send_message(chat_id, p_chat_ops.Help.commands, parse_mode= 'Markdown')
        
@bot.message_handler(commands=['create_pl'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, p_chat_ops)
        bot_create_playlist(bot, g_ops, chat_id, p_chat_ops, playlist_title)
        
@bot.message_handler(commands=['drop_pl'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, p_chat_ops)
        bot_drop_playlist(bot, g_ops, chat_id, p_chat_ops, playlist_title)

@bot.message_handler(commands=['link'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, p_chat_ops)
        bot_get_url(bot, g_ops, chat_id, p_chat_ops, playlist_title)

@bot.message_handler(content_types=['text'], chat_types=['private'])
def get_text_messages(message):
    if message.date > bot_time_start:
        mes_txt = message.text
        chat_id = message.from_user.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, p_chat_ops)
        
        if(mes_txt.lower().find('дай ссылку') >= 0):
            bot_get_url(bot, g_ops, chat_id, p_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('удали плейлист') >= 0):
            bot_drop_playlist(bot, g_ops, chat_id, p_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('создай плейлист') >= 0):
            bot_create_playlist(bot, g_ops, chat_id, p_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('https') >= 0):
            bot_add_track_to_playlist(bot, g_ops, chat_id, p_chat_ops, playlist_title, mes_txt)        

if __name__ == "__main__":
    while True:
        try:
            print(dttm(), 'BOT STARTED','\n')
            bot_time_start = time.mktime(datetime.now().timetuple())
            if(g_ops.tg_admin_id):bot.send_message(g_ops.tg_admin_id, 'Я ожил!')
            
            # Цикл жизни
            bot.polling()
            
            print(dttm(), 'BOT DOWN','\n')
            if(g_ops.tg_admin_id):bot.send_message(g_ops.tg_admin_id, 'Я прилег!')
            
        except Exception as e:
            if(g_ops.tg_admin_id):bot.send_message(g_ops.tg_admin_id, 'Я прилег! ' + str(e))
            print(dttm(), 'BOT DOWN','\n')
            print(dttm(), e)
