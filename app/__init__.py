import logging
import os
from flask import Flask
from config import Config
from config import DECODER_JS_TEMPLATE_PATH
from config import DECODER_JS_PATH
from config import VALIDATOR_REGEX
from flask_bootstrap import Bootstrap5, SwitchField
from flask_gridify import FlaskGridify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect

#from flask_sqlalchemy import SQLAlchemy

def create_app(config_class=Config):
    #set validators for client side ,patch JS decoder
    #add validators to js template file, save as a main file
    with open(DECODER_JS_PATH,"w",encoding="utf-8") as jsf:
        for (k,v) in VALIDATOR_REGEX.items():	
            js_line = "const " + k +  "=/" + v + '/g;'    
            jsf.write(js_line + "\n")
        js_line_all_validators = "const valid_regex = [" + ",".join(VALIDATOR_REGEX) + "];"    
        jsf.write(js_line_all_validators+"\n");    
        #the rest of the code comes from template
        with open(DECODER_JS_TEMPLATE_PATH,"r",encoding="utf-8") as jsft:    
            jsf.write(jsft.read())
            
    #set supported languages
    #for lang in config_class.LANGUAGE_SUPPORT:
        

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