from flask import Blueprint

bp = Blueprint('decoder', __name__,template_folder='templates',static_folder='static',static_url_path='/static/decoder')

from app.decoder import routes