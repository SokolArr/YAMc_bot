import telebot
from telebot import types
from helpers.getPL import get_playlists, get_playlist,get_uid_playlist
from helpers.addTrack import add_track
from helpers.parseLink import parse_link
import re
import time
import json

TG_KEY = None
try:
    f = open('./bot/tg_key.json')
    data = json.load(f)
    TG_KEY = str(data['TG_KEY'])
    f.close()
except:
    print('Error TG_KEY')
    
bot = telebot.TeleBot(TG_KEY)
TOKEN = ''

@bot.message_handler(commands=['start'])
def start(message):
    time.sleep(2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/start")
    btn2 = types.KeyboardButton("/init")
    markup.add(btn1)
    markup2.add(btn2)
    
    bot.send_message(message.from_user.id, "👋 Привет! Я тут за музыку 🎵 Яндекса шарю!\n") 
    bot.send_message(message.from_user.id, "Жмякай кнопку /init чтобы начать общение 🌚", reply_markup=markup2)

@bot.message_handler(commands=['init'])
def init(message):
    time.sleep(2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/init")
    btn2 = types.KeyboardButton('Меню')
    markup.add(btn1)
    markup2.add(btn2)
    is_in_db = is_in_id_token(message.from_user.id)
    if(is_in_db == False):
        bot.send_message(message.from_user.id, "🔐 Напиши мне свой YAM token", reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, "🌍 Получить можно по: https://chrome.google.com/webstore/detail/yandex-music-token/lcbjeookjibfhjjopieifgjnhlegmkib")
        bot.send_message(message.from_user.id, "🔠 Формат такой: y0_AgAAAAA1S4TYAaG8XgoAAADvqsoGymMpoD8EqkCTRL1JjsQWe4o9IQs")
        bot.register_next_step_handler(message, get_input_token)
    if(is_in_db == True):
        bot.send_message(message.from_user.id, '⚠️ Вы уже прислали токен\nПерейдите в меню', reply_markup=markup2)
        
@bot.message_handler(commands=['prefs'])
def prefs(message):
    time.sleep(2)
    is_in_db = is_in_id_token(message.from_user.id)
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Удалить TOKEN")
    btn2 = types.KeyboardButton('Меню')
    markup.add(btn2)
    if(is_in_db == False):
        bot.send_message(message.from_user.id, "🔐 Напиши мне свой YAM token", reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, "🌍 Получить можно по: https://chrome.google.com/webstore/detail/yandex-music-token/lcbjeookjibfhjjopieifgjnhlegmkib")
        bot.send_message(message.from_user.id, "🔠 Формат такой: y0_AgAAAAA1S4TYAaG8XgoAAADvqsoGymMpoD8EqkCTRL1JjsQWe4o9IQs")
        bot.register_next_step_handler(message, get_input_token)
    if(is_in_db == True):
        markup1.add(btn1)
        bot.send_message(message.from_user.id, "⚙️ Вот что можно настроить...", reply_markup=markup1)
    
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    time.sleep(2)
    if message.text == 'Удалить TOKEN' and get_token_by_id(message.from_user.id) != 'none':
        print('user', message.from_user.id, 'want to edit token')
        print(message.from_user.id, 'start delete TOKEN')
        del_token(str(message.from_user.id)+';'+ str(get_token_by_id(message.from_user.id)), message)
        
    if message.text == 'Меню' and get_token_by_id(message.from_user.id) != 'none':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        btn1 = types.KeyboardButton('Покажи плейлисты')
        btn2 = types.KeyboardButton('Добавь трек')
        btn3 = types.KeyboardButton('/init')
        btn4 = types.KeyboardButton('/prefs')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, 'Вы в меню', reply_markup=markup)
        
    if message.text == 'Покажи плейлисты' and get_token_by_id(message.from_user.id) != 'none':
        bot.send_message(message.from_user.id, 'Показываю...') #ответ бота
        bot.send_message(message.from_user.id, str(get_pl(get_token_by_id(message.from_user.id)))) #ответ бота
        
    elif message.text == 'Добавь трек' and get_token_by_id(message.from_user.id) != 'none':
        bot.send_message(message.from_user.id, '🔗 Кинь ссылку на трек, а потом album_id через ">"\n' +
                                               'Пример:', reply_markup=types.ReplyKeyboardRemove()) #ответ бота
        bot.send_message(message.from_user.id, 'https://music.yandex.ru/album/27268450/track/117130808?utm_medium=copy_link>1016') #ответ бота

        bot.register_next_step_handler(message, add_tr_handler)
           
    elif get_token_by_id(message.from_user.id) == 'none':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/init")
        markup.add(btn1)
        bot.send_message(message.from_user.id, '❗️ Нужна процедура инициализации TOKEN\nЖми /init', reply_markup=markup) #ответ бота
    
def get_input_token(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    print('message.chat.id:', message.chat.id,'message.message_id' ,message.message_id)
    TOKEN = str(message.text)
    try:
        state = write_token(message.from_user.id, TOKEN)
        if(state):
            bot.send_message(message.from_user.id, "✅ TOKEN запомнил, твое сообщение с ним удалил 🥸 ",  reply_markup=markup)
        else: bot.send_message(message.from_user.id, "⚠️ Токен " + get_token_by_id(message.from_user.id) + " уже в базе, если нужно исправить обращайся к админу", reply_markup=markup)
        time.sleep(1)
        bot.delete_message(message.chat.id, message.message_id)
    except: 
        time.sleep(1)
        bot.delete_message(message.chat.id, message.message_id)
        print('Eror add token')
      
def write_token(id: str, token: str):
    to_inc = str(id) + ';' + str(token) + ';\n'
    # print('before: \n',f.readlines())
    if (is_in_id_token(id) == False):   
        f = open('./bot/id_token.txt','a')
        f.write(to_inc)
        f.close()
        print('New user', id, 'added')
        return True
    elif (is_in_id_token(id) == True):
        print(id, ' already in base!')
        return False
    # f = open('./bot/id_token.txt','r')    
    # print('after: \n', f.readlines())
    # f.close()
    
    
def get_token_by_id(id: str):
    f = open('./bot/id_token.txt','r')
    list_of_vals = f.readlines()
    f.close()
    answ = 'none'
    for i in range(0, len(list_of_vals)):
        splitted_str = list_of_vals[i].split(';')
        if splitted_str[0] == str(id):
            answ = str(splitted_str[1])
    return answ

def is_in_id_token(id: str):
    f = open('./bot/id_token.txt','r')
    list_of_vals = f.readlines()
    f.close()
    answ = False
    for i in range(0, len(list_of_vals)):
        splitted_str = list_of_vals[i].split(';')
        if splitted_str[0] == str(id):
            answ = True
    return answ

def get_pl(TOKEN: str):
    USERID= ''
    try:
        playlists = get_playlists(TOKEN, USERID)
        to_return = 'Title, album_id\n'
        for i in range(0, len(playlists)):
            to_return = to_return +str(playlists[i]['title']) + ', ' + str(playlists[i]['kind']) + '\n'
        return to_return
    except:
        print('Error watch playlist')
        return '❗️ Ошибка, не могу чекнуть плейлисты, отправь корректный TOKEN'

def add_tr_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    try:
        parsed_link = parse_link(message.text, '>')
        answ = add_tr(get_token_by_id(message.from_user.id), parsed_link)
        bot.send_message(message.from_user.id, str(answ), reply_markup=markup)
    except: 
        bot.send_message(message.from_user.id, '❗️ Введи корректную ссылку, как в примере' , reply_markup=markup)
        print('ERROR parse link:', message.text)
    
      
def add_tr(TOKEN, parsed_link):
    USERID = ''
    try:
        kind = parsed_link['kind']
        USERID = get_uid_playlist(TOKEN, str(kind))
        add_track(TOKEN, USERID, parsed_link)
        return '✅ Закинул, проверяй!\n'
    except:
        return '❗️ ОшибОчка не могу закинуть трек, проверь TOKEN\n'

def del_token(key_todel: str, message):
    try:
        with open('./bot/id_token.txt') as f:
            lines = f.readlines()
        str = key_todel
        arch_del = []
        pattern = re.compile(re.escape(str))
        with open('./bot/id_token.txt', 'w') as f:
            for line in lines:
                result = pattern.search(line)
                if result is not None:
                    arch_del.append(result)
                if result is None:
                    f.write(line)
        print('keys was deleted:\n', arch_del)
        bot.send_message(message.from_user.id, '⚠️ Твой TOKEN удален!')
    except:
        bot.send_message(message.from_user.id, '❗️ Ошибка удаления TOKEN')
        print('ERROR to del TOKEN')

bot.polling() #обязательная для работы бота часть



