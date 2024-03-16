class GlobalOptions:
    def __init__(self, token, ya_usr_id, tg_key, bot_tag, tg_admin_id = None, dev_mode = None):
        self.token          = token
        self.ya_usr_id      = ya_usr_id
        self.tg_key         = tg_key
        self.bot_tag        = bot_tag
        self.tg_admin_id    = tg_admin_id
        self.dev_mode       = dev_mode
        
    def print_prefs(self):
        print(self.token, self.ya_usr_id, self.tg_key, self.bot_tag, self.tg_admin_id, self.dev_mode)
        
    def get_mode(self):
        return self.dev_mode
    
class ChatOptions:
    class Greeting:
        main = "👋 Привет! Я могу сделать общий плейлист в Яндекс Музыке!\n Чтобы узнать как введи /help"
        
    class Help:
        about_send  = "⚠️ Отправь мне ссылку на трек в формате:\n" \
                    + "`https://music.yandex.ru/album/670787/track/6098621`\nИ я добавлю трек в общий плейлист"
        commands    = "Я понимаю команды: \n\
/link или `дай ссылку` - вернет 🔗 ссылку на плейлист \n\
/create\_pl или `создай плейлист` - ✅ создаст плейлист \n\
/drop\_pl или `удали плейлист` - ❌ удалит плейлист"
    
    class Answ:
        add_track       = "✅ Закинул трек в плейлист\n"
        get_url         = "✅ Готово:\n"
        delete_playlist = "✅ Удалил\n"
        create_playlist = "✅ Создал плейлист!\n"
        no_playlist     = "✅ У тебя не было общего плейлиста, я создал его и закинул туда трек\n"
        
    class ChatError:
        hash_gen                = "🚫 Ошибка в генерации хеша"
        add_track               = "🚫 Ошибка в добавлении трека"
        create_playlist         = "🚫 Ошибка в создании плейлиста"
        no_playlist             = "🚫 Не нашел твой плейлист! Попробуй создать его,\nпопроси меня добавить трек.\nЧтобы узнать как, введи /help для помощи"
        already_have_playlist   = "🚫 Плейлист уже был создан! Вот ссылка:\n"
        nothing_to_del          = "🚫 Нечего удалять! Сначала надо его создать,\nпопроси добавить трек:\nВведи /help для помощи"
        parse_link              = "🚫 Не могу прочитать ссылку, проверь корректность\n"
        get_group_info          = "🚫 Ошибка получения информации о группе\n"
        no_right_edit_topics    = "🚫 Боту необходимо выдать право редактировать топики!\n"
    
    class ConsoleError:
        hash_gen        = '- ERROR to get hash:'
        create_playlist = '- ERROR to create playlist:'
        add_track       = '- ERROR add track:'
        nothing_to_del  = '- ERROR nothing to delete:'
        parse_link      = '- ERROR parse link:'
        no_playlist     = '- ERROR no playlist fetch:'
        get_group_info  = "- ERROR bad try to get group info"
            
PrivateChatOptions = ChatOptions
    
class GroupChatOptions(ChatOptions):
    class Help:
        def __init__(self, bot_tag = None):
            self.bot_tag = bot_tag
            
        def get_commands(self):
            string = "Я понимаю команды: \n\
/link или `"+ self.bot_tag + " дай ссылку` - вернет 🔗 ссылку на общий плейлист \n\
/create\_pl или `"+ self.bot_tag + " создай плейлист` - ✅ создаст общий плейлист \n\
/drop\_pl или `"+ self.bot_tag + " удали плейлист` - ❌ удалит общий плейлист"
            return string
            
        def get_about_send(self):
            return "⚠️ Отправь мне ссылку на трек в формате:\n`" \
            + self.bot_tag + " https://music.yandex.ru/album/670787/track/6098621`\nИ я добавлю трек в общий плейлист"
            
class SuperGroupChatOptions(GroupChatOptions):  
    class Greeting:
        main = '👋 Привет! я создал для себя отдельный топик, общайся со мной тут пожалуйста :)\nВведи /help чтобы узнать мои команды'
        main2 = "👋 Привет! Я могу сделать общий плейлист в Яндекс Музыке!\n Чтобы узнать как введи /help.\n🏷️ А еще, можно включить в темы в группе, что бы со мной было удобно общаться в подходящем разделе.\nДля корректной работоспособности бота, ему надо выдать права администратора на управление темами группы!"

        