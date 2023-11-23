import os
from logging import INFO
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

DB_PATH  = os.path.join(basedir, "airports.db")
DB_PATH_URL  = f'sqlite:///{DB_PATH}'

SEPARATOR = "."
AIRPORTS = {
    "BGSF":"Сенре Стремфьорд",
    "ORL":"Орландо",
    "LGW":"Гатвик",
    "YVR":"Янктон",
    "SEA":"Сиэтл"}
MONTHS_RU = {   
    "JAN": "январь",
    "FEB": "февраль",
    "MAR": "март",
    "APR": "апрель",
    "MAY": "май",
    "JUN": "июнь",
    "JUL": "июль",
    "AUG": "август",
    "SEP": "сентябрь",
    "OCT": "октябрь",
    "NOV": "ноябрь",
    "DEC": "декабрь",
    "ЯНВ": "январь",
    "ФЕВ": "февраль",
    "МАР":  "март",
    "АПР":  "апрель",
    "МАЙ":  "май",
    "ИЮН": "июнь",
    "ИЮЛ":  "июль",
    "АВГ": "август",
    "СЕН": "сентябрь",
    "ОКТ": "октябрь",
    "НОЯ": "ноябрь",
    "ДЕК": "декабрь"
    }

MONTHS_EN = {   
    "JAN": "January",
    "FEB": "February",
    "MAR": "March",
    "APR": "April",
    "MAY": "May",
    "JUN": "June",
    "JUL": "July",
    "AUG": "August",
    "SEP": "September",
    "OCT": "October",
    "NOV": "November",
    "DEC": "December",
    "ЯНВ": "January",
    "ФЕВ": "February",
    "МАР":  "March",
    "АПР":  "April",
    "МАЙ":  "May",
    "ИЮН": "June",
    "ИЮЛ":  "July",
    "АВГ": "August",
    "СЕН": "September",
    "ОКТ": "October",
    "НОЯ": "November",
    "ДЕК": "December"
    }


YEAR_PREFIX = "20"

DECODER_JS_TEMPLATE_PATH = os.path.join(basedir,"app","decoder","static","decoder.js.template")
DECODER_JS_PATH = os.path.join(basedir,"app","decoder","static","decoder.js")                                        
VALIDATOR_REGEX = {
#	номер рейса
'valid_flight' : '(?:(?<=^)|(?<=\.)|(?<=\s))[1-9,A-Z,А-Я][A-Z,А-Я,1-9]\s{0,1}[ ,-]{0,1}\d{3,4}(?=\s|$)',
#	маршрут
'valid_route' : '(?:(?<=^)|(?<=\.)|(?<=\s))(([A-Z,А-ЯЁ]{3,4})([A-Z,А-ЯЁ]{3,4}))(?=\s|$)',
#	дата 
'valid_date' :  '(?:(?<=^)|(?<=\.)|(?<=\s))((\d{2})([A-Z,А-ЯЁ]{3})(\d{2}){0,1})(?=\s|$)',
#	время вылета и прилета в 2 группы
#	с прилетом на следующий день в отдельной группе
'valid_time' : '(?:(?<=^)|(?<=\.)|(?<=\s))(\d{4})\s{1,}(\d{4})(\+1){0,1}(?=\s|$)'
}

class Config:
    DEBUG = True
    LOGGING_LEVEL = INFO
    LOGGING_FILE = 'logs/app.log'
    LOG_WITH_GUNICORN = True
    SECRET_KEY = secrets.token_urlsafe(16)
    SQLALCHEMY_DATABASE_URI = DB_PATH_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGE_SUPPORT = ['en','ru']
    PREPOPULATE_DB_FILE  = "prep.csv"