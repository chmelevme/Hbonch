from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from webapp.models import User
from flask_login import current_user


class change_pass(FlaskForm):
    old_password = PasswordField('Введите старый пароль', validators=[DataRequired()])
    pasword = PasswordField('Введите новый пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сменить пароль')

    def validate_old_pass(self, old_password):
        if not current_user.check_password(old_password.data):
            raise ValidationError('Старый пороль ввелён неверно')


class change_name(FlaskForm):
    name = StringField('Введите новое имя', validators=[DataRequired()])
    submit = SubmitField('Сменить имя')


class change_mail(FlaskForm):
    mail = StringField('Введите новую почту', validators=[DataRequired(), Email()])
    submit = SubmitField('Сменить почту')

    def validate_mail(self, mail):
        user = User.query.filter_by(email=mail.data).first()
        if user is not None:
            raise ValidationError('Данная почта уже зарегистрированна')
