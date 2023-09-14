import os
from logging import INFO
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

DB_PATH  = f'sqlite:///{os.path.join(basedir, "airports.db")}'
SEPARATOR = "."
AIRPORTS = {
    "BGSF":"Сенре Стремфьорд",
    "ORL":"Орландо",
    "LGW":"Гатвик",
    "YVR":"Янктон",
    "SEA":"Сиэтл"}
MONTHS = {   
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
    "DEC": "декабрь"
    }
YEAR_PREFIX = "20"

class Config:
    DEBUG = True
    LOGGING_LEVEL = INFO
    LOGGING_FILE = 'logs/app.log'
    SECRET_KEY = secrets.token_urlsafe(16)
    SQLALCHEMY_DATABASE_URI = DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False