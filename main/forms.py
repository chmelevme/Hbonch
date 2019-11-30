from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import ValidationError, DataRequired
from webapp.models import Level, Group
from datetime import datetime


class create_deadline(FlaskForm):
    group_name = StringField(validators=[DataRequired()])
    value = StringField(validators=[DataRequired()])
    title = StringField(validators=[DataRequired()])
    expiration_date = DateField(validators=[DataRequired()])

    def validate_expiration_date(self, expiration_date):
        now = datetime.utcnow()
        if expiration_date < now:
            raise ValidationError('Дедлайн уже прошёл')

    def validate_value(self, value):
        value = Level.query.filter_by(value=value.data).first()
        if value is None:
            raise ValidationError('Не верный формат стоимости')

    def validate_group(self, group_name):
        group = Group.query.filter_by(name=group_name.data).first()
        if group is None:
            raise ValidationError('Не верная группа')
