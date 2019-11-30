from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import ValidationError, DataRequired
from flask_login import current_user
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

