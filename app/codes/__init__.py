import os
from flask import Blueprint
from flask import Flask , current_app
from flask_gridify import FlaskGridify
from .models import Airport
from flask import current_app
from config import DB_PATH

bp = Blueprint('codes', __name__,template_folder='templates')

#current_app.logger.info(get_db_url())
#current_app.logger.info(get_db_path())

with current_app.app_context():
    dbe = current_app.config['db'] 
    if not os.path.exists(DB_PATH):
        inspector = sa.inspect(dbe)
        if not inspector.has_table("airport"):
            dbe.drop_all()
            dbe.create_all()
            current_app.logger.info('Initialized the database!')
        else:
            app.logger.info('Database already contains the airport table.')
            #dbe.create_all()
    grid = FlaskGridify(current_app,flask_sqlalchemy_db=dbe, root_url_prefix='/grids')#, per_page_size=10)
    grid.gridify(Airport)    
    
    #db.session.add(Airport())
    #db.session.commit()
    
from . import views, models
from app.codes import routes