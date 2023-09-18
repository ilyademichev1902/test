from app.codes import bp
from flask import render_template,jsonify,request
from app.processing import  gdsdecoder

@bp.route('/codes')
def codes():
    return render_template("grid.html.jinja")
    
@bp.route('/list_decoded/<language>/',defaults={'language':'EN'},methods=['POST'])
@bp.route('/list_decoded/<language>/',methods=['POST'])
def list_decoded(language):
    #print(request.full_path)
    if (request.method == 'POST'):
        language_str = str(language)
        data_in = request.get_json()
        print(data_in)
        data_lines = data_in.splitlines()
        for line in data_lines:
            out = gdsdecoder.decode_gds(line)
            print(line)        
        data_out = {}
        if language_str == 'EN':
            data_out = {
                'language':language,
                'data':'EN LANGUAGE TEST',
                'errors':['Test error EN 1','Test error EN 2']
            }
        elif language_str == 'RU':
            data_out = {
                'language':language,
                'data':'RU LANGUAGE TEST',                
                'errors':['Test error RU 1']
            }
        else:          
            data_out = {
                'language':language,
                'data':'',                
                'errors':'Language not supported'
            }
    print(data_out)
    return jsonify(data_out)