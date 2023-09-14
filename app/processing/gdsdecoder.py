from app.processing import processors
from flask import current_app
test_sample  ="IO-297 N 28APR23 ORLBGSF HS1 2040 0015"
def decode_gds(sample):
    decoded = ["рейс"]
    try:
        s = sample.split()
        flight_code = s[0]
        date = s[2]
        from_to_airports = s[4]
        from_time=s[6]
        to_time=s[7]
        decoded.append( flight_code )
        try:
            processors.process_airports(from_to_airports,decoded)
        except KeyError:
            return 'Аэропорт не найден в базе'
        try:
            processors.process_date(date,decoded)
        except ValueError:
            return 'Ошибка в формате даты'
        try:
            processors.process_time(from_time,decoded)
        except ValueError:        
           return 'Ошибка в формате времени'
        try:
            processors.process_time(to_time,decoded)
        except ValueError:        
           return 'Ошибка в формате времени'
    except KeyError:
        return 'Ошибка недостаточно полей в строке'

    return  " ".join(decoded)

if __name__ == '__main__':
    print(decode_gds(test_sample))

