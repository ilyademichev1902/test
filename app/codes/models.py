from sqlalchemy import Column, Integer,String  
from flask import current_app

class Airport(current_app.config['db'].Model):
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True)
    code = Column("Код",String(4), unique=True)
    ru_airport_name = Column("Название(русский)",String(65))
    en_airport_name = Column("Название(англ)",String(65))


