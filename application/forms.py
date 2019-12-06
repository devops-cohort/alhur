from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users
from flask_login import LoginManager, current_user

class PostForm(FlaskForm):
    title = StringField('Title',
        validators=[
                DataRequired(),
                Length(min=4, max=100)
        ]
    )
    content = StringField('Content',
        validators=[
                DataRequired(),
                Length(min=4, max=500)
        ]
    )
    submit = SubmitField('Post Content')

class TeamForm(FlaskForm):
    TeamName = StringField('Team Name', validators=[DataRequired(),Length(min=1, max=18)])
    Pokemon1Data = StringField('Lead Pokemon', validators=[DataRequired(), Length(min=1, max=3)] )
    Pokemon2Data = StringField('Second Pokemon',validators=[DataRequired(), Length(min=1, max=3)])
    Pokemon3Data = StringField('Third Pokemon',validators=[DataRequired(), Length(min=1, max=3)])
    Pokemon4Data = StringField('Fourth Pokemon',validators=[DataRequired(), Length(min=1, max=3)])
    Pokemon5Data = StringField('Fifth Pokemon',validators=[DataRequired(), Length(min=1, max=3)])
    Pokemon6Data = StringField('Last Pokemon',validators=[DataRequired(), Length(min=1, max=3)])
    submit = SubmitField('Create Team')
                                    
            
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    first_name = StringField('First Name',
        validators=[
                DataRequired(),
                Length(min=2, max=30)
        ]
    )
    last_name = StringField('Last Name',
        validators=[
                DataRequired(),
                Length(min=2, max=30)
        ]
    )
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use')
    submit = SubmitField('Update')
