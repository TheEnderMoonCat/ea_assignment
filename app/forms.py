from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import User, products, companys


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class ProductForm(FlaskForm):
    PN = StringField(_l('Product Name'), validators=[DataRequired()])
    PURL = StringField(_l('PhotoURL'), validators=[DataRequired()])
    URL = StringField(_l('Website URL'), validators=[DataRequired()])
    loc = StringField (_l('Location'), validators=[DataRequired()])
    Price = StringField(_l('Price'), validators=[DataRequired()])
    UPPrice = StringField(_l('UPPrice'), validators=[DataRequired()])
    Intro = TextAreaField(_l('Introduction'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def validate_PN(self, PN):
        ProductName = products.query.filter_by(PN=PN.data).first()
        if ProductName is not None:
            raise ValidationError(_('Please use a different Product Name.'))


class CompanysForm(FlaskForm):
    CName = StringField(_l('Company Name'), validators=[DataRequired()])
    CURL = StringField(_l('Company URL'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def validate_CName(self, CName):
        CompanyName = companys.query.filter_by(CName=CName.data).first()
        if CompanyName is not None:
            raise ValidationError(_('Please use a different Company Name.'))