class GlobalOptions:
    def __init__(self, token, ya_usr_id, tg_key, bot_tag, tg_admin_id = None):
        self.token          = token
        self.ya_usr_id      = ya_usr_id
        self.tg_key         = tg_key
        self.bot_tag        = bot_tag
        self.tg_admin_id    = tg_admin_id
    
class ChatOptions:
    class Greeting:
        main = "👋 Привет! Я могу сделать общий плейлист в Яндекс Музыке!\n Чтобы узнать как введи /help"
        
    class Help:
        about_send  = "🔗 Отправь мне ссылку на трек в формате:\n`" \
                    + " https://music.yandex.ru/album/29998108/track/123237014`\nИ я добавлю трек в общий плейлист"
        commands    = "⚠️ Я понимаю команды:\n" \
                    + "🔗 `дай ссылку` - вернет ссылку на плейлист\n" \
                    + "✅ `создай плейлист` - создаст плейлист\n" \
                    + "❌ `удали плейлист`  - удалит плейлист"
    
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
    
    class ConsoleError:
        hash_gen        = '- ERROR to get hash:'
        create_playlist = '- ERROR to create playlist:'
        add_track       = '- ERROR add track:'
        nothing_to_del  = '- ERROR nothing to delete:'
        parse_link      = '- ERROR parse link:'
        no_playlist     = '- ERROR no playlist fetch:'
            
PrivateChatOptions = ChatOptions
    
class GroupChatOptions(ChatOptions):
    class Help:
        def __init__(self, bot_tag = None):
            self.bot_tag = bot_tag
            
        def get_commands(self):
            return "⚠️ Я понимаю команды:\n🔗 `" + self.bot_tag \
            + " дай ссылку` - вернет ссылку на плейлист\n✅ `" \
            + self.bot_tag + " создай плейлист` - создаст плейлист\n❌ `" \
            + self.bot_tag + " удали плейлист`  - удалит плейлист"
        def get_about_send(self):
            return "🔗 Отправь мне ссылку на трек в формате:\n`" \
            + self.bot_tag + " https://music.yandex.ru/album/29998108/track/123237014`\nИ я добавлю трек в общий плейлист"