from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm): #initializing a form class SignupForm inherited from FlaskForm class (used for creating forms in WTForms extension)
    email = StringField('Email', validators=[DataRequired(), Email()]) #initializing a form field for String with 'email' input type which can't be blank
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)]) #initializing a form field for String with 2-50 symbols which can't be blank
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)]) #initializing a form field for Password which can't be blank


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()]) # initializing a form field for TextArea, which can't be blank
