# YAMc_bot
Бот для телеграм, позволяющий создавать общие плейлисты.

# Quick start

Для работы необходимо создать файл `bot/creds.py` c переменными следующего вида:

+ `TOKEN = 'XXXXX'` - Аутентификационный токен ЯМ
+ `YA_USR_ID = 'XXXXX'` - Имя аккаунта ЯМ на котором будут созданы общие плейлисты
+ `TG_KEY = 'XXXXX'` - Ключ выдаваемый BotFather при регистрации бота
+ `BOT_TAG = '@XXXXX'` - Тэг бота (имя), используется при обращении в группах
+ `TG_ADMIN_ID = XXXXXX` - _Не обязательный параметр. Нужен только для логирования доверенному лицу о старте и падении бота_
  
Выполнить запуск `$ python3.11 YAMc_bot/bot/main.py`

# Security
Бот не собирает персональные данные пользователя.\
Весь код находится в открытом доступе и предствлен в текущем репозитории.
