
from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired

class institute_update_form(FlaskForm):
    Institute_name=StringField('Institute Name',validators=[DataRequired()])
    identity=StringField('identity',validators=[DataRequired()])
    address=StringField('address',validators=[DataRequired()])
    contact=StringField('contact',validators=[DataRequired()])
    psycho=StringField('psycho',validators=[DataRequired()])
    
    submit = SubmitField('Submit')


class authentications(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
   
    submit = SubmitField('Submit')    


# class personal_update_form_(FlaskForm):
#     id_institute=StringField('id_institute',validators=[DataRequired()])
#     file_name=StringField('file_name',validators=[DataRequired()])
    
#     submit = SubmitField('Submit')     



class personal_update_form(FlaskForm):
    standard=StringField('standard',validators=[DataRequired()])
    id_institute=StringField('id_institute',validators=[DataRequired()])
    batch=StringField('batch',validators=[DataRequired()])
    file_name=StringField('file_name',validators=[DataRequired()])
    
    submit = SubmitField('Submit')      