from helpers.yam_api            import *
from helpers.yam_link_parser    import *
from helpers.bot_api            import *
from helpers.utils.bot_logger   import *
from options.chat_options       import *
from options.global_options     import GlobalOptions
from creds                      import creds_ops

import telebot
import time

global_ops          = GlobalOptions(**creds_ops)
privat_chat_ops     = PrivateChatOptions
group_chat_ops      = GroupChatOptions
supergroup_chat_ops = SuperGroupChatOptions
bot                 = telebot.TeleBot(global_ops.tg_key)

# Групповые чаты
@bot.message_handler(commands=['start'], chat_types=['group'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        bot.send_message(chat_id, group_chat_ops.Greeting.main) 
        
@bot.message_handler(commands=['help'], chat_types=['group'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        bot.send_message(chat_id, group_chat_ops.Help(global_ops.bot_tag).get_about_send(), parse_mode= 'Markdown')
        bot.send_message(chat_id, group_chat_ops.Help(global_ops.bot_tag).get_commands(), parse_mode= 'Markdown')

@bot.message_handler(commands=['create_pl'], chat_types=['group'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, group_chat_ops)
        bot_create_playlist(bot, global_ops, chat_id, group_chat_ops, playlist_title)
        
@bot.message_handler(commands=['drop_pl'], chat_types=['group'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, group_chat_ops)
        bot_drop_playlist(bot, global_ops, chat_id, group_chat_ops, playlist_title)

@bot.message_handler(commands=['link'], chat_types=['group'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, group_chat_ops)
        bot_get_url(bot, global_ops, chat_id, group_chat_ops, playlist_title)
        
@bot.message_handler(content_types=['text'], chat_types=['group'])
def get_text_messages(message):
    if message.text[0:len(global_ops.bot_tag)] == global_ops.bot_tag and message.date > bot_time_start:
        mes_txt = message.text[len(global_ops.bot_tag)+1:]
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, group_chat_ops)
        
        if(mes_txt.lower().find('дай ссылку') >= 0):
            bot_get_url(bot, global_ops, chat_id, group_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('удали плейлист') >= 0):
            bot_drop_playlist(bot, global_ops, chat_id, group_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('создай плейлист') >= 0):
            bot_create_playlist(bot, global_ops, chat_id, group_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('https') >= 0):
            bot_add_track_to_playlist(bot, global_ops, chat_id, group_chat_ops, playlist_title, mes_txt)


# Супергрупповые чаты
@bot.message_handler(commands=['start'], chat_types=['supergroup'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        try:
            if str(bot.get_chat(chat_id)).find("'is_forum': True") > 0:
                topic = bot.create_forum_topic(chat_id, global_ops.bot_tag, 13338331, '5310045076531978942')
                bot.send_message(chat_id, supergroup_chat_ops.Greeting.main, message_thread_id = eval(topic.__str__())['message_thread_id'])
            else:
                bot.send_message(chat_id, supergroup_chat_ops.Greeting.main2)
                
        except Exception as e:
            if (str(e).find("not enough rights to create a topic") > 0):
                bot.send_message(chat_id, supergroup_chat_ops.ChatError.no_right_edit_topics)
            else:
                bot.send_message(chat_id, supergroup_chat_ops.ChatError.get_group_info)
                print(dttm(), chat_id, supergroup_chat_ops.ConsoleError.get_group_info, str(e))
        
@bot.message_handler(commands=['help'], chat_types=['supergroup'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        thread_id = message.message_thread_id
        bot.send_message(chat_id, supergroup_chat_ops.Help(global_ops.bot_tag).get_about_send(), parse_mode= 'Markdown', message_thread_id = thread_id)
        bot.send_message(chat_id, supergroup_chat_ops.Help(global_ops.bot_tag).get_commands(), parse_mode= 'Markdown', message_thread_id = thread_id)

@bot.message_handler(commands=['create_pl'], chat_types=['supergroup'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        thread_id = message.message_thread_id
        playlist_title = bot_get_title_hash_all_for_supergroup(bot, chat_id, thread_id, supergroup_chat_ops)
        bot_create_playlist_for_supergroup(bot, global_ops, chat_id, thread_id, supergroup_chat_ops, playlist_title)
        
@bot.message_handler(commands=['drop_pl'], chat_types=['supergroup'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        thread_id = message.message_thread_id
        playlist_title = bot_get_title_hash_all_for_supergroup(bot, chat_id, thread_id, supergroup_chat_ops)
        bot_drop_playlist_for_supergroup(bot, global_ops, chat_id, thread_id, supergroup_chat_ops, playlist_title)

@bot.message_handler(commands=['link'], chat_types=['supergroup'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        thread_id = message.message_thread_id
        playlist_title = bot_get_title_hash_all_for_supergroup(bot, chat_id, thread_id, supergroup_chat_ops)
        bot_get_url_for_supergroup(bot, global_ops, chat_id, thread_id, supergroup_chat_ops, playlist_title)
        
@bot.message_handler(content_types=['text'], chat_types=['supergroup'])
def get_text_messages(message):
    if message.text[0:len(global_ops.bot_tag)] == global_ops.bot_tag and message.date > bot_time_start:
        mes_txt = message.text[len(global_ops.bot_tag)+1:]
        chat_id = message.chat.id
        thread_id = message.message_thread_id
        playlist_title = bot_get_title_hash_all_for_supergroup(bot, chat_id, thread_id, supergroup_chat_ops)
        
        if(mes_txt.lower().find('дай ссылку') >= 0):
            bot_get_url_for_supergroup(bot, global_ops, chat_id, thread_id, supergroup_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('удали плейлист') >= 0):
            bot_drop_playlist_for_supergroup(bot, global_ops, chat_id, thread_id, supergroup_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('создай плейлист') >= 0):
            bot_create_playlist_for_supergroup(bot, global_ops, chat_id, thread_id, supergroup_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('https') >= 0):
            bot_add_track_to_playlist_for_supergroup(bot, global_ops, chat_id, thread_id, supergroup_chat_ops, playlist_title, mes_txt)
            
        
# Private чаты
@bot.message_handler(commands=['start'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.from_user.id
        bot.send_message(chat_id, privat_chat_ops.Greeting.main) 

@bot.message_handler(commands=['help'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.from_user.id
        bot.send_message(chat_id, privat_chat_ops.Help.about_send, parse_mode= 'Markdown')
        bot.send_message(chat_id, privat_chat_ops.Help.commands, parse_mode= 'Markdown')
        
@bot.message_handler(commands=['create_pl'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, privat_chat_ops)
        bot_create_playlist(bot, global_ops, chat_id, privat_chat_ops, playlist_title)
        
@bot.message_handler(commands=['drop_pl'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, privat_chat_ops)
        bot_drop_playlist(bot, global_ops, chat_id, privat_chat_ops, playlist_title)

@bot.message_handler(commands=['link'], chat_types=['private'])
def start(message):
    if message.date > bot_time_start:
        chat_id = message.chat.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, privat_chat_ops)
        bot_get_url(bot, global_ops, chat_id, privat_chat_ops, playlist_title)

@bot.message_handler(content_types=['text'], chat_types=['private'])
def get_text_messages(message):
    if message.date > bot_time_start:
        mes_txt = message.text
        chat_id = message.from_user.id
        playlist_title = bot_get_title_hash_all(bot, chat_id, privat_chat_ops)
        
        if(mes_txt.lower().find('дай ссылку') >= 0):
            bot_get_url(bot, global_ops, chat_id, privat_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('удали плейлист') >= 0):
            bot_drop_playlist(bot, global_ops, chat_id, privat_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('создай плейлист') >= 0):
            bot_create_playlist(bot, global_ops, chat_id, privat_chat_ops, playlist_title)
                
        elif(mes_txt.lower().find('https') >= 0):
            bot_add_track_to_playlist(bot, global_ops, chat_id, privat_chat_ops, playlist_title, mes_txt)        

if __name__ == "__main__":
    while True:
        try:
            write_log('BOT STARTED')
            bot_time_start = time.mktime(datetime.now().timetuple())
            if(global_ops.tg_admin_id):bot.send_message(global_ops.tg_admin_id, 'Я ожил!')
            
            # Цикл жизни
            bot.polling()
            
            write_log('BOT DOWN', state='Error')
            if(global_ops.tg_admin_id):bot.send_message(global_ops.tg_admin_id, 'Я прилег!')
            
        except Exception as e:
            if(global_ops.tg_admin_id):bot.send_message(global_ops.tg_admin_id, 'Споткнулся об:\n' + str(e))
            write_log('BOT DOWN WITH ERROR:', exception=e)
