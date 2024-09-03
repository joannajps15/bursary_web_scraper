from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class EnterData(FlaskForm):

    year = StringField('Year', validators=[DataRequired()])
    term = StringField('Term', validators=[DataRequired()])
    program = StringField('Program', validators=[DataRequired()])
    athlete = BooleanField('Are you an athelete?')

    submit = SubmitField('S U B M I T') 


