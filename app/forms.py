# app/forms.py
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    TextAreaField, IntegerField, FloatField,
    BooleanField, SelectField
)
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username  = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    name      = StringField('Name',     validators=[DataRequired(), Length(max=120)])
    email     = StringField('Email',    validators=[DataRequired(), Email()])
    password  = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm   = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField('Register')

class LoginForm(FlaskForm):
    username  = StringField('Username', validators=[DataRequired()])
    password  = PasswordField('Password', validators=[DataRequired()])
    submit    = SubmitField('Login')

class ProfileForm(FlaskForm):
    description     = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    parish          = StringField('Parish', validators=[DataRequired(), Length(max=100)])
    biography       = TextAreaField('Biography', validators=[Length(max=1000)])
    sex             = SelectField('Sex', choices=[('Male','Male'),('Female','Female')])
    race            = StringField('Race', validators=[Length(max=50)])
    birth_year      = IntegerField('Birth Year', validators=[DataRequired()])
    height          = FloatField('Height (inches)', validators=[DataRequired()])
    fav_cuisine     = StringField('Favorite Cuisine', validators=[Length(max=100)])
    fav_colour      = StringField('Favorite Colour', validators=[Length(max=50)])
    fav_school_sub  = StringField('Favorite School Subject', validators=[Length(max=100)])
    political       = BooleanField('Political')
    religious       = BooleanField('Religious')
    family_oriented = BooleanField('Family Oriented')
    submit          = SubmitField('Save Profile')
