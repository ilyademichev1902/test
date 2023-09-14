from flask import current_app
import config
import re
def process_airports(from_to_airports,decoded):
    current_app.logger.info("from_to_airports:"+str(from_to_airports))
    if len(from_to_airports) == 6:
        from_airport = from_to_airports[:3]
        to_airport = from_to_airports[3:]
    elif len(from_to_airports) == 8:
        from_airport = from_to_airports[:4]
        to_airport = from_to_airports[4:]
    else: #7
        #case 1
        from_airport = from_to_airports[:3]
        to_airport = from_to_airports[3:]    

        current_app.logger.info("CASE 1 from_airport:"+from_airport)
        current_app.logger.info("CASE 1 to_airport:"+to_airport)

        try:
            from_airport  = config.AIRPORTS[from_airport]
            to_airport = config.AIRPORTS[to_airport]
        except KeyError as e:
            
            current_app.logger.info("Wrong case : 3 to 4")
            #case 2
            from_airport = from_to_airports[:4]
            to_airport = from_to_airports[4:]    

            current_app.logger.info("CASE 2 from_airport:"+from_airport)
            current_app.logger.info("CASE 2 to_airport:"+to_airport)

            try:
                from_airport  = config.AIRPORTS[from_airport]
                to_airport = config.AIRPORTS[to_airport]
            except KeyError as e:

                current_app.logger.info("Wrong case : 4 to 3")
                current_app.logger.error("No matching airports")
                raise ValueError
    decoded.append(from_airport)
    decoded.append(to_airport)

def process_date(date,decoded):
    day = None
    year = None
    month = None
    try:
        cre = re.compile("\d+")
        date_partial =  cre.findall(date)
        day = date_partial[0]
        #print(day)
        year = config.YEAR_PREFIX + date_partial[1]
        #print(year)
        cre = re.compile("\D+")
        date_partial =  cre.findall(date)
        month = config.MONTHS[date_partial[0]]
    except Exception as e:
        print("Invalid date")
        raise ValueError
    decoded.extend([day,month,year])

def process_time(time_,decoded):
    try:
        decoded.append( time_[:2] + config.SEPARATOR  + time_[2:] )
    except KeyError:
        raise ValueError
    