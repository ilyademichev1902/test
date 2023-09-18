import logging
import os
from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap5, SwitchField
from flask_gridify import FlaskGridify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect

#from flask_sqlalchemy import SQLAlchemy

def create_app(config_class=Config):
    app = Flask(__name__)    
    app.config.from_object(config_class)

    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler = logging.FileHandler(app.config['LOGGING_FILE'])
        file_handler.setLevel(app.config['LOGGING_LEVEL'])
        app.logger.addHandler(file_handler)
    
    db = SQLAlchemy(app)
        
    app.config['db']  = db 

    bootstrap = Bootstrap5(app)

    #db = SQLAlchemy(app)
    #csrf = CSRFProtect(app)
    # Initialize Flask extensions here

    # Register blueprints here

    from app.decoder import bp as decoder_bp
    app.register_blueprint(decoder_bp)#,template_folder='templates')

    with app.app_context():
        from app.codes import bp as codes_bp
        app.register_blueprint(codes_bp)#,template_folder='templates')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask  Airport Application</h1>'
    
    #app.logger.info(str(app.url_map).join("\n"")
    
    return app