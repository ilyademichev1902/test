from app.decoder import bp
from flask import render_template,session,redirect
from .forms import GDSDecoderForm

@bp.route('/',methods=['GET', 'POST'])
def decoder():
    gds_input = None
    form = GDSDecoderForm()
    #print(form)
    if form.validate_on_submit():
        session['gds_input'] = form.gds_input.data
        session['decoder_out'] = decode_gds(session.get('gds_input'))
        return redirect(url_for('decoder'))            
    return render_template("decoder.html",form=form)
    if session.get('gds_input'):
        form.gds_input.data=session.get('gds_input')     
        form.decoder_out.data=session.get('decoder_out')
    else:
        form.decoder_out.data=''
    
    #session.clear()    
    return render_template('decoder.html', form=form)

   