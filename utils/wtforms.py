from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, ValidationError, Length

from models.controllers import TeacherAuthController

msg = {
    'email': 'Некорректный e-mail',
    'psw': 'Пароль должен быть от 6 до 15 символов.',
    'full_name': 'быть на кириллице и содержать хотя бы одну заглавную букву.',
}


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(msg['email'])], description="example@gmail.com")
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=15, message=msg['psw'])], description="*******")
    remember = BooleanField('Запомнить', default=False)

    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired(), Regexp('^[А-ЯЁ][а-яё]*$', message=f'Фамилия должна {msg["full_name"]}')], description="Иванов")
    first_name = StringField('Имя', validators=[DataRequired(), Regexp('^[А-ЯЁ][а-яё]*$', message=f'Имя должно {msg["full_name"]}')], description="Иван")
    middle_name = StringField('Отчество', validators=[DataRequired(), Regexp('^[А-ЯЁ][а-яё]*$', message=f'Отчество должно {msg["full_name"]}')], description="Иванович")

    email = StringField('Email', validators=[DataRequired(), Email('Некорректный email')], description="example@gmail.com")
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=15, message=msg['psw'])], description="*******")
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают.'), Length(min=6, max=15, message=msg['psw'])], description="*******")

    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        if TeacherAuthController.get_teacher_auth(email=self.email.data):
            raise ValidationError('Преподователь с таким email уже зарегистрирован')
