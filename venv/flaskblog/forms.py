from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField, TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flaskblog.models import User
from flask_wtf.file import FileAllowed,FileField
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField(label='Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField(label='Email',validators = [DataRequired(),Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField(label = 'Sign Up')

    def validate_username(self,username):
        """
                Validate existanse of username
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is occupated. Please choose another one.')


    def validate_email(self,email):
        """
                Validate existanse of email
        """

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is registered. Please choose unique one.')

    def validate_password(self,password):
        """
                Custom validation of password
        """
        pass

class LoginForm(FlaskForm):
    email = StringField(label='Email',validators = [DataRequired(),Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField(label = 'Log In')

class UpdateAccountForm(FlaskForm):
    username = StringField(label='Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField(label='Email',validators = [DataRequired(),Email()])
    picture = FileField(label='Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField(label = 'Update Profile')

    def validate_username(self,username):
        """
                Validate existanse of username
        """
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is occupated. Please choose another one.')


    def validate_email(self,email):
        """
                Validate existanse of email
        """
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is registered. Please choose unique one.')

class PostForm(FlaskForm):
    title = StringField(label='Title',validators=[DataRequired()])
    content = TextAreaField(label='Title',validators=[DataRequired()])
    submit = SubmitField(label='Post')

class SendResetForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label = 'Send Reset Email')


class PasswordResetForm(FlaskForm):
    password = PasswordField(label='New Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm New Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField(label = 'Change Password')


