from wtforms import TextAreaField,StringField, SubmitField,RadioField,FieldList,SelectField
from wtforms.widgets.core import ListWidget,RadioInput
from wtforms.validators import InputRequired, Regexp
from flask_wtf import FlaskForm
VALID_PNR = r"^\w{2}\s{0,1}\d{3,4}\s\w\s\w{5}\s\d\s\w{6}\s\w{3}\s+\w{4}\s\w{4}(\+1){0,1}\s+\w{3}\s\w\s\d$"


class GDSDecoderForm(FlaskForm):
    #RadioField('Язык имени аэропорта:', choices=[('value','description'),('value_two','whatever')])
    gds_input = TextAreaField('', validators=[InputRequired()],render_kw={"oninput":"instant_decoder()"})
    decoder_out = TextAreaField('')
    submit = SubmitField('Декодировать')
    #_fields = [ gds_input,decoder_out,submit   ]
    #user = 'a'
    # def __init__(self,  *args, **kwargs):
        # self.sel.choices = [(1,1)]
        #self.user = user
