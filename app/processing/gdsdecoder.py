from app.processing import processors
from flask import current_app
import re
from config import VALIDATOR_REGEX

test_sample  ="IO-297 N 28APR23 ORLBGSF HS1 2040 0015"

def decode_gds(sample,language,errors):
    #decoded = ["рейс"]
    decoded = {}    
    current_app.logger.info(sample)
    current_app.logger.info(language)
    for (_,v) in VALIDATOR_REGEX.items():
        # current_app.logger.info(v)
        current_app.logger.info(re.findall(re.compile(v),sample))
        current_app.logger.info(len(re.findall(re.compile(v),sample)))
        
    if all([len(re.findall(re.compile(validator),sample)) == 1 for validator in VALIDATOR_REGEX.values()]):
        flight_code = re.findall(re.compile(VALIDATOR_REGEX['valid_flight']),sample)[0]
        from_to_airports = re.findall(re.compile(VALIDATOR_REGEX['valid_route']),sample)[0][0]
        date =  re.findall(re.compile(VALIDATOR_REGEX['valid_date']),sample)[0]
        from_to_time = re.findall(re.compile(VALIDATOR_REGEX['valid_time']),sample)[0]
        from_time  = from_to_time[0]
        to_time = from_to_time[1]
        #(from_time, to_time) = re.sub(' +', ' ', from_to_time).split(" ") #remove repetitive spaces
        decoded['flight_code'] = flight_code 
        decoded_airports = []
        processors.process_airports(from_to_airports,language,decoded_airports,errors)
        decoded['from_airport'] = decoded_airports[0]
        decoded['to_airport'] = decoded_airports[1]
        decoded['day'],decoded['month'],decoded['year' ]= processors.process_date(date,language,errors)
        decoded['from_time'] = processors.process_time(from_time,errors)
        decoded['to_time'] = processors.process_time(to_time,errors)

        #return  " ".join(decoded)
        airport_max_str_length = 30
        current_app.logger.info(decoded)
        #return "test"
        #рейс   SU-1480                  Sheremetyevo-Emelyanovo 20   октябрь 2023 20.35-05.05
        # route = "-".join(decoded[1:3])
        # times = "-".join(decoded[6:]) 
        # #{route:>2*airport_max_str_length}                        
        # return f"{decoded[0]:>7}{decoded[3]:>3}{decoded[4]:>10}{decoded[5]:>6} {times:10} {route:30}"
        return decoded
    else:
        errors.append(sample + "\n" + "Cтрока не соответствует формату. Отсутвует одно из полей.")        
        return
        

if __name__ > '__main__':
    errors=[]
    print(decode_gds(test_sample,'RU',errors))
    print(errors)

