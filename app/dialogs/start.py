# -*- coding: utf-8 -*-

__all__ = ['start', 'description', 'help', 'langs', 'commands', 'tests', 'begin', 'stop']

import re

from app.settings import DEFAULT_LANGUAGE, DEFAULT_PARSE_MODE, STARTMENU, TESTNAMES
from app.handlers import *

_design_mode = 'menu' # 'commands'

_QUESTIONS = {
    'ru': (
"""
<b>Здравствуйте!</b>
<b>Вы работаете с Telegram-Ботом "TVMLiveHealthBot". 
Спасибо, что обратились к нам!</b>
""",
"""
<b>Описание и возможности.</b>

А) объяснение возможностей этого самого нашего чудо-бота.
Б) сообщение, что он, бот, понимает обратившегося и может ему помочь.
В) что у него, бота, есть свой метод.
""",
"""
<b>Команды Бота.</b>

/start: Начало работы.
/clear: Очистить результаты предыдущих тестов.
/description: Краткое описание и наши возможности.
/commands: Список команд клинической беседы.
/tests: Психологические тесты.
/lang: Выбор языка.
/version: Версия ПО.
""",
"""
<b>Клиническая беседа.</b>

/begin: Начать диалог.
/qN: Переход к вопросу N диалога.
/end: Завершить диалог.
""",
"""
Хорошо. Давайте, продолжим...
""",
"""
Для начала диалога нажмите /begin.
""",
"""
<b>Психологические тесты:</b>
""",
"""
<b>Язык диалога.</b>

/ru: RU
/ua: UA
""",
"""
Для начала нашей беседы, пожалуйста, введите команду /begin.
Для выбора теста на психологическое состояние /tests. 
Помощь по работе с ботом /help.
""",
"""
Вашему вниманию предлагается (добавить описание главного меню):
""",
), 
    'ua': (
"""
<b>Доброго дня!</b>
<b>Ви працюєте с Telegram-ботом "TVMLiveHealthBot". 
Дякуємо, що звернулися до нас!</b>
""",
"""
<b>Опис і можливості.</b> 

А) пояснення можливостей цього самого нашого чудо-бота.
Б) повідомлення, що він, бот, розуміє звернувся і може йому допомогти.
В) що у нього, бота, є свій метод.
""",
"""
<b>Команди Бота.</b>

/start: Початок роботи.
/clear: Очистити результати попередніх тестів.
/description: Короткий опис і наші можливості.
/commands: Список команд клінічної бесіди.
/tests: Психологічні тести.
/lang: Вибір мови.
/version: Версія ПО.
""",
"""
<b>Клінічна бесіда:</b>

/begin: Почати діалог.
/qN: Перехід до питання N діалогу. 
/end: Завершити діалог.
""",
"""
Чудово. Давайте продовжимо...
""",
"""
Для початку бесіди натисніть, будь-ласка кнопку /begin.
""",
"""
<b>Психологічні тести:</b>
""",
"""
<b>Мова діалогу.</b>

/ru: RU
/ua: UA
""",
"""
Для початку нашої бесіди, будь ласка, натисніть команду /begin, 
Для вибору тесту на психологічний стан /tests. 
Допомога по роботі з ботом  /help.
""",
"""
Вашій увазі пропонується (додати опис головного меню): 
""",
),
}

def get_question(i, lang, no_eof=None):
    s = _QUESTIONS[lang][i].strip()
    return no_eof and re.sub(r'\n', ' ', s) or s

def start(bot, message, logger=None, **kw):
    lang = kw.get('lang')
    bot.reply_to(message, get_question(0, lang, no_eof=False), parse_mode=DEFAULT_PARSE_MODE)

    if _design_mode == 'menu':
        send_inline_keyboard(bot, message, STARTMENU[lang][0], get_question(9, lang))
        help(bot, message, logger=logger, **kw)

def description(bot, message, logger=None, **kw):
    bot.reply_to(message, get_question(1, kw.get('lang'), no_eof=False), parse_mode=DEFAULT_PARSE_MODE)

def help(bot, message, logger=None, **kw):
    mode = kw.get('mode')
    text = get_question(2, kw.get('lang'))

    if mode == 1:
        bot.send_message(message.chat.id, text, parse_mode=DEFAULT_PARSE_MODE)
    else:
        bot.reply_to(message, text, parse_mode=DEFAULT_PARSE_MODE)

def langs(bot, message, logger=None, **kw):
    bot.reply_to(message, get_question(7, kw.get('lang')), parse_mode=DEFAULT_PARSE_MODE)

def commands(bot, message, logger=None, **kw):
    bot.reply_to(message, get_question(3, kw.get('lang')), parse_mode=DEFAULT_PARSE_MODE)

def tests(bot, message, logger=None, **kw):
    lang = kw.get('lang')
    items = TESTNAMES[lang]
    text = get_question(6, lang)+'\n'

    if _design_mode == 'menu':
        obs = []
        for k in sorted(items.keys()):
            name = items[k]
            obs.append((name, '/%s' % k))
        send_inline_rows_keyboard(bot, message, obs, text)
    else:
        for k in sorted(items.keys()):
            name = items[k]
            text += '\n/%s: %s.' % (k, name)
        bot.reply_to(message, text, parse_mode=DEFAULT_PARSE_MODE)

def begin(bot, message, logger=None, **kw):
    bot.reply_to(message, get_question(4, kw.get('lang'), no_eof=True))

def stop(bot, message, logger=None, **kw):
    bot.reply_to(message, get_question(5, kw.get('lang'), no_eof=True))
