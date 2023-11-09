from app.codes import bp
from flask import render_template,jsonify,request
from app.processing import  gdsdecoder
from flask import current_app
import json
@bp.route('/codes')
def codes():
    return render_template("grid.html.jinja")
    
@bp.route('/list_decoded/<language>/',defaults={'language':'EN'},methods=['POST'])
@bp.route('/list_decoded/<language>/',methods=['POST'])
def list_decoded(language):
    #print(request.full_path)
    if (request.method == 'POST'):
        language_str = str(language).lower()
        data_in = request.get_json()
        #print(data_in)
        data_lines = data_in#.splitlines()
        errors = []
        out = []
        if language_str in current_app.config["LANGUAGE_SUPPORT"]:

            for line in data_lines:
                out.append( gdsdecoder.decode_gds(line , language_str, errors) )
                #current_app.logger.info(out)
                #current_app.logger.info(errors)        

            current_app.logger.info(out)
            current_app.logger.info(errors)        
            
            data_out = {}
        
            data_out = {
                'language':language,
                'data': json.dumps(out),
                'errors':errors
            }
        else:          
            data_out = {
                'language':language,
                'data':'',                
                'errors':'Язык не поддерживается'
            }
    return jsonify(data_out)