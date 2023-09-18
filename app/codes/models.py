from sqlalchemy import Column, Integer,String  
from flask import current_app

class Airport(current_app.config['db'].Model):
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True)
    Code = Column(String(4), unique=True)
    Ru = Column(String(65))
    En = Column(String(65))


