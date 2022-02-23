# -*- coding: utf-8 -*-

import re
import random
import json
from datetime import datetime

# https://pypi.org/project/user-agents/
#from user_agents import parse as user_agent_parse

from flask import (
    Response, render_template, url_for, redirect, request, make_response, 
    jsonify, flash, stream_with_context, g, current_app
)
from flask_login import login_required, current_user
from flask_babel import gettext

from config import (
    CONNECTION,
    IsDebug, IsDeepDebug, IsTrace, IsShowLoader, IsForceRefresh, IsPrintExceptions, IsNoEmail, 
    basedir, errorlog, print_to, print_exception,
    default_unicode, default_encoding,
    LOCAL_EASY_DATESTAMP, getCurrentDate,
    is_webhook,
)

product_version = '1.02, 2021-10-08 (Python3, Redis)'

#########################################################################################

#   -------------
#   Default types
#   -------------

DEFAULT_LANGUAGE = 'ua'
DEFAULT_PARSE_MODE = 'HTML'
DEFAULT_PER_PAGE = 10
DEFAULT_PAGE = 1
DEFAULT_UNDEFINED = '---'
DEFAULT_DATE_FORMAT = ('%d/%m/%Y', '%Y-%m-%d',)
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d< %H:%M:%S'
DEFAULT_DATETIME_INLINE_FORMAT = '<nobr>%Y-%m-%d</nobr> <nobr>%H:%M:%S</nobr>'
DEFAULT_DATETIME_INLINE_SHORT_FORMAT = '<nobr>%Y-%m-%d</nobr><br><nobr>%H:%M</nobr>'
DEFAULT_DATETIME_TODAY_FORMAT = '%d.%m.%Y'
DEFAULT_HTML_SPLITTER = ':'

BEGIN = (
    'dialogs.begin',
    )

SCENARIO = (
    ('dialogs.person', None),
    ('dialogs.gender', None),
    ('dialogs.age', None),
    ('dialogs.occupation', None),
    ('dialogs.education', None),
    ('dialogs.marital_status', None),
    ('dialogs.children', None),
    ('dialogs.upbringing', None),
    ('dialogs.childhood', None),
    ('dialogs.family', None),
    ('dialogs.relationships', None),
    ('dialogs.discomfort', None),
    ('dialogs.stress', None),
    ('dialogs.grievance', 23),
    )

TESTS = (
    ('', None),
    ('dialogs.ptest1', 'T1',),
    ('dialogs.ptest2', 'T2',),
    ('dialogs.ptest3', 'T3',),
    ('dialogs.ptest4', 'T4',),
    ('dialogs.ptest5', 'T5',),
    ('dialogs.ptest6', 'T6',),
    ('dialogs.ptest7', 'T7',),
    ('dialogs.ptest8', 'T8',),
    ('dialogs.ptest9', 'T9',),
    ('dialogs.ptest10', 'T10',),
    ('dialogs.ptest11', 'T11',),
    ('dialogs.ptest12', 'T12',),
    ('dialogs.ptest13', 'T13',),
    )

TESTNAMES = {
    'ru': {
        'T1'  : 'Госпитальная шкала тревоги и депрессии (HADS)',
        'T2'  : 'Индивидуально-типологический опросник Собчик (ИТО)',
        'T3'  : 'Измерение уровня депрессии (BDI)',
        'T4'  : 'Уровень тревожности Бека',
        'T5'  : 'Острая реакция на стресс',
        'T6'  : 'Шкала депрессии Цунга',
        'T7'  : 'Определение характеристик темперамента',
        'T8'  : 'Тревожность Тейлора',
        'T9'  : 'Уровень социальной фрустрированности Вассермана',
        'T10' : 'Шкала реактивной и личностной тревожности Спилбергера-Ханина',
        'T11' : 'Эмоциональное выгорание Бойко',
        'T12' : 'Мотивация к успеху Реана',
        'T13' : 'Эмоциональное выгорание Маслач',
    },
    'ua': {
        'T1'  : 'Госпітальна шкала тривоги та депресії (HADS)',
        'T2'  : 'Індивідуально-типологічний опитувальник Собчик (ІТО)',
        'T3'  : 'Вимірювання рівня депресіїТест (BDI)',
        'T4'  : 'Рівень тривожності Бека',
        'T5'  : 'Гостра реакція на стрес',
        'T6'  : 'Шкала депресії Цунга',
        'T7'  : 'Визначення характеристик темпераменту',
        'T8'  : 'Тривожність Тейлора',
        'T9'  : 'Рівень соціальної фрустрованність Васермана',
        'T10' : 'Шкала реактивної і особистісної тривожності Спілбергера-Ханіна',
        'T11' : 'Емоційне вигорання Бойко',
        'T12' : 'Мотивацію до успіху Реана',
        'T13' : 'Психологічне вигорання Маслач',
    },
}

STARTMENU = {
    'ru': [
        (('Доверительная беседа', 'begin:0'), ('Психологические тесты', 'tests:0')), 
        (('', '')),
    ],
    'ua': [
        (('Довірлива бесіда', 'begin:0'), ('Психологічні тести', 'tests:0')), 
        (('', '')),
    ],
}

THANKS = (
    'dialogs.thanks',
    )

END = (
    'dialogs.end',
    )

NO_RESULTS = 'not enough results'
NO_DATA = 'no data'


def tests_count():
    return len(TESTS)
