import os
import csv
import platform
from subprocess import check_output
from flask import Blueprint
from flask import Flask , current_app
from flask_gridify import FlaskGridify
from .models import Airport
from flask import current_app
from config import DB_PATH
from sqlalchemy import MetaData, Table

bp = Blueprint('codes', __name__,template_folder='templates')

#current_app.logger.info(get_db_url())
#current_app.logger.info(get_db_path())

def prepopulate():
    pfn = current_app.config['PREPOPULATE_DB_FILE']
    dbe = current_app.config['db'].engine 
    metadata = MetaData()
    metadata.reflect(dbe, only=['airport'])
    airport_table = Table('airport', metadata, autoload=True, autoload_with=dbe)
    insert_query = airport_table.insert()
    if os.path.exists(pfn):
        with open(pfn, 'r', encoding="utf-8") as pf_csv:
            csv_reader = csv.reader(pf_csv, delimiter=';')
            header = next(csv_reader)
            values  = [{"Code": row[0], "Ru": row[1], "En": row[2]} 
                       for row in csv_reader]
            insertstmt = insert_query.values(values)#.returning(airport_table.c.id)
            result = dbe.execute(insertstmt)            
            current_app.logger.info(f'Database prepopulated.')# Inserted: {result.rowcount}')
    else:                
        current_app.logger.info('Prepopulate CSV file is not specified in PREPOPULATE_DB_FILE')

#implement patch for long grid 20000 items
PATCH_PATH = '.venv\Lib\site-packages\flask_restless\manager.py'
is_windows = any(platform.win32_ver())
#current_app.logger.info(any(platform.win32_ver()))
if not is_windows:
    cmd = 'which'
    out = check_output([cmd, ' -a python3']) 
    current_app.logger.info(out)
#    open('')
# else:    
    # cmd = 'dir'
    # out = check_output([cmd, '/Q']) 
    # current_app.logger.info(out)
            
with current_app.app_context():
    dbe = current_app.config['db'] 
    current_app.logger.info(DB_PATH)
    if not os.path.isfile(DB_PATH):
        dbe.drop_all()
        dbe.create_all()
        prepopulate()
        current_app.logger.info('Initialized the database!')
    else:
        current_app.logger.info('Database already exists.')
 
    grid = FlaskGridify(current_app,flask_sqlalchemy_db=dbe, root_url_prefix='/grids')#, per_page_size=10)
    grid.gridify(Airport)#,column_names=['a','b','c'])    
    
    
from . import views, models
from app.codes import routes