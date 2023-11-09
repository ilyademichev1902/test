import config
import re

from flask import current_app
from app.codes.models import Airport
# from sqlalchemy.orm import Session
# from sqlalchemy import select
 
def translate_airport(airport_code,language,decoded,errors):
   with current_app.app_context():
        dbe = current_app.config['db']
        # with Session(dbe) as session:
        #     kwargs = {
        #         '{0}__{1}'.format('name', 'startswith'): 'A',
        #         '{0}__{1}'.format('name', 'endswith'): 'Z'
        #     }
        #     fa = session.query(Airport).filter(Airport.Code == airport_code).all()
        #     if len(fa) == 0:
        #         errors.append("Аэропорт  {} не найден. Обновите базу.".format(from_airport))
        #     else:
        #         decoded.append(fa[0])       

def process_airports(from_to_airports,language,decoded_airports,errors):

    def match_airport(airport):
        # from_airport_encoded  = config.AIRPORTS[from_airport]
        # decoded.append(from_airport_encoded)
        # to_airport_encoded = config.AIRPORTS[to_airport]
        with current_app.app_context():  
            res = Airport.query.filter_by(Code=airport).first()      
            # with Session( current_app.config['db'].engine ) as session: 
            #     stmt = session.select(Airport).where(Airport.Code == airport)
            #     res = session.execute(stmt)
            if not res:
                decoded_airports.append(airport)
                raise ValueError(airport)
            else:
                if language=='ru':
                    decoded_airports.append(res.Ru)
                if language=='en':
                    decoded_airports.append(res.En)
                return                    

    current_app.logger.info("from_to_airports:"+str(from_to_airports))

    length = len(from_to_airports) 
    if length > 8 or length < 6:
        errors.append("Рейс больше 8ми символов или меньше 6ти.:"+from_to_airports)
        return
    elif length == 6 or length == 8:
        from_airport, to_airport = from_to_airports[:length//2], from_to_airports[length//2:]        
        current_app.logger.info("CASE 0 from_airport:"+from_airport)
        current_app.logger.info("CASE 0 to_airport:"+to_airport)
        try:
            match_airport(from_airport)
            match_airport(to_airport)
        except ValueError as e:
            current_app.logger.info("Wrong case : 0")
            current_app.logger.error("No matching airport:"+e.args[0])
            errors.append("Аэропорт не найден:"+e.args[0])                
        return #symmetric case completed
    elif length == 7:
        #assymetric case  length==7
        #if airport string is of 7 characters
        #case 1 : 3 characters to first ,4 to second
        from_airport = from_to_airports[:3]
        to_airport = from_to_airports[3:]    

        current_app.logger.info("CASE 1 from_airport:"+from_airport)
        current_app.logger.info("CASE 1 to_airport:"+to_airport)

        try:
                match_airport(from_airport)
                match_airport(to_airport)
        except ValueError as e:
            current_app.logger.info("Wrong case : 3 to 4")
            current_app.logger.error("No matching airport:"+e.args[0])
            errors.append("Аэропорт не найден:"+e.args[0])

            #case 2: 4 characters to first, 3 to second
            from_airport = from_to_airports[:4]
            to_airport = from_to_airports[4:]    

            current_app.logger.info("CASE 2 from_airport:"+from_airport)
            current_app.logger.info("CASE 2 to_airport:"+to_airport)

            try:
                match_airport(from_airport)
                match_airport(to_airport)
            except ValueError as e:
                current_app.logger.info("Wrong case : 4 to 3")
                current_app.logger.error("No matching airport:"+e.args[0])
                errors.append("Аэропорт не найден:"+e.args[0])
            return #assymetric case completed

    
def process_date(date,errors):
    day = None
    year = None
    month = None
    #cre = re.compile("\d+")
    #date_partial =  cre.findall(date)
    day = date[1]
    if int(day) < 1 or int(day) > 31:
        errors.append("Ошибка в дне даты. День больше 31 или меньше 1: "+date[1])
    year = ''  if date[3]=='' else config.YEAR_PREFIX + date[3]
    #cre = re.compile("\D+")
    #date_partial =  cre.findall(date)
    month = config.MONTHS.get(date[2], None)
    current_app.logger.info(month)
    if month is None:
        errors.append("Ошибка в месяце даты." + date[2])
        month = date[2]
    return (day,month,year)

def process_time(time_,errors):
    if len(time_[:2])  < 2 or ( int(time_[:2])<0 or int(time_[:2]) > 23):
        errors.append("Ошибка в времени, неверно указан час: " + time_[:2])
    elif len(time_[2:])  < 2 or ( int(time_[2:])<0 or int(time_[2:]) > 59):
        errors.append("Ошибка в времени, неверно указана минута: " + time_[2:])        
    else:
        return time_[:2] + config.SEPARATOR  + time_[2:] 
    