from flask_wtf import FlaskForm
from datetime import datetime, date, timedelta
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from wtforms import StringField, EmailField, PasswordField, BooleanField, TextAreaField, \
    IntegerField, FloatField, FieldList, DateTimeLocalField, DateField, FileField, SubmitField


class LoginForm(FlaskForm):
    email = EmailField(
        'E-mail:', validators=[DataRequired()], description='example@mail.ru', default='ernest@mail.ru')
    # TODO: Поменять на PasswordField
    password = StringField(
        'Пароль:', validators=[DataRequired(), Length(min=6, max=36)],
        description='example123', default='string')
    rememberMe = BooleanField('Запомнить меня', default=False)

    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    def validate_password(self, field):
        if field.data != self.repeatPassword.data:
            raise ValidationError()

    def validate_repeatPassword(self, field):
        if field.data != self.password.data:
            raise ValidationError('Пароли не совпадают')

    firstName = StringField('Имя:', validators=[DataRequired(), Length(max=50)], description='Иван', default="Иван")
    lastName = StringField('Фамилия:', validators=[DataRequired(), Length(max=50)], description='Иванов',
                           default="Иванов")
    middleName = StringField('Отчество:', validators=[DataRequired(), Length(max=90)], description='Иванович',
                             default="Иванович")
    birthday = DateField('Дата рождения:', validators=[DataRequired()], description='дд.мм.гггг',
                         default=date(year=2000, month=5, day=14))

    email = EmailField(
        'E-mail:', validators=[DataRequired()], description='example@mail.ru', default='ivan@mail.ru')

    # TODO: Поменять на PasswordField
    password = StringField(
        'Пароль:', validators=[DataRequired(), Length(min=6, max=36)],
        description='example123', default='string')

    repeatPassword = StringField(
        'Подтверждение пароля:', id='repeatPassword', name='repeatPassword',
        validators=[DataRequired(), Length(min=6, max=36)],
        description='example123', default='string')

    submit = SubmitField('Зарегистрироваться')


class EventCreateForm(FlaskForm):
    name = StringField('Название:', id='name', name='name', validators=[DataRequired(), Length(max=150)],
                       default="Квартирник от Сали",)
    description = TextAreaField('Описание:', id='description', name='description', validators=[Length(max=1500)],
                                default='Описание мероприятия', )  # render_kw={'rows': 12, 'class': 'description'}
    expectedAmount = FloatField('Цель сбора (₽):', id='expectedAmount', name='expectedAmount', validators=[DataRequired()],
                                default=10000)  # NumberRange(min=0, max=100000)
    recommendedDonation = IntegerField('Рекомендованный донат (₽):', id='recommendedDonation', name='recommendedDonation',
                                       validators=[DataRequired(), NumberRange(min=0, max=5000)], default=300, )
    countOfMembers = IntegerField('Кол-во участников:', id='countOfMembers', name='countOfMembers',
                                  validators=[DataRequired()], default=25, )
    concession = TextAreaField('Концессии (необязательно):', id='concession', name='concession', validators=[Length(max=650)],
                               default='Продажа мороженного и мерча')
    startDateTime = DateTimeLocalField('Начало:', id='startDateTime', name='startDateTime',
                                       validators=[DataRequired()], format='%Y-%m-%dT%H:%M',
                                       default=datetime(year=2023, month=5, day=14, hour=15))

    endDateTime = DateTimeLocalField('Окончание:', id='endDateTime', name='endDateTime',
                                     validators=[DataRequired()], format='%Y-%m-%dT%H:%M',
                                     default=datetime(year=2023, month=5, day=15, hour=15))

    venueName = StringField('Название:', name='venueName', id='venueName', validators=[DataRequired(), Length(max=150)],
                            default="Квартира Сали")
    venueDescription = TextAreaField('Описание места:', id='venueDescription', name='venueDescription',
                                     validators=[Length(max=800)], default='Уютный уголок:3')
    address = StringField('Улица, дом:', id='address', name='address', validators=[DataRequired(), Length(max=150)],
                          default="ул. Пушкина, 10")
    seats = IntegerField('Кол-во сидячих мест:', id='seats', name='seats', validators=[DataRequired(), NumberRange(min=0)],
                         default=0)
    country = StringField('Страна:', id='country', name='country', validators=[DataRequired(), Length(max=150)],
                          default="Россия")
    state = StringField('Регион:', id='state', name='state', validators=[DataRequired(), Length(max=150)],
                        default="Республика Крым")
    city = StringField('Город:', id='city', name='city', validators=[DataRequired(), Length(max=150)],
                       default="Симферополь")

    submit = SubmitField('Создать мероприятие', id='submit')

    def validate_countOfMembers(form, field):
        min_count = 1
        max_count = 100
        if field.data < min_count:
            raise ValidationError(f'Минимальное кол-во участников: {min_count}')
        if field.data > max_count:
            raise ValidationError(f'Максимальное кол-во участников: {max_count}')

    def validate_expectedAmount(form, field):
        min_amount = 0
        max_amount = 500000
        if field.data < min_amount:
            raise ValidationError(f'Минимальная сумма для сбора: {min_amount}')
        if field.data > max_amount:
            raise ValidationError(f'Максимальная сумма для сбора: {max_amount}')

    # def validate_endDateTime(self, field):
    #     for i, end_time in enumerate(field.data):
    #         if field.data[i] <= self.startDateTime.data[i]:
    #             raise ValidationError(
    #                 f'Дата и время окончания должны быть позже даты и времени начала (для записи {i + 1})')
    #             # f'Дата и время окончания должны быть позже даты и времени начала')
    def validate_endDateTime(self, field):
        if field.data <= self.startDateTime.data:
            raise ValidationError(
                f'Дата и время окончания должны быть позже даты и времени начала')
        week_after_start = self.startDateTime.data + timedelta(days=7)
        if field.data > week_after_start:
            raise ValidationError(
                'Дата и время окончания должны быть не позднее, чем через неделю после даты и времени начала')


# TODO: edit event позже
# class EventEditForm(FlaskForm):
#     name = StringField('Название:', id='name', name='name', validators=[DataRequired(), Length(max=150)],)
#     description = TextAreaField('Описание:', id='description', name='description', validators=[Length(max=800)],)
#     countOfMembers = IntegerField('Кол-во участников:', id='countOfMembers', name='countOfMembers',
#                                   validators=[DataRequired()], default=25, )
#     expectedAmount = FloatField('Цель сбора:', id='expectedAmount', name='expectedAmount', validators=[DataRequired()],)  # NumberRange(min=0, max=100000)
#     venueName = StringField('Название:', name='venueName', id='venueName', validators=[DataRequired(), Length(max=150)],)
#     venueDescription = TextAreaField('Описание места:', id='venueDescription', name='venueDescription',
#                                      validators=[Length(max=800)])
#     address = StringField('Улица, дом:', id='address', name='address', validators=[DataRequired(), Length(max=150)],)
#     country = StringField('Страна:', id='country', name='country', validators=[DataRequired(), Length(max=150)],
#                           default="Россия")
#     state = StringField('Регион:', id='state', name='state', validators=[DataRequired(), Length(max=150)],)
#     city = StringField('Город:', id='city', name='city', validators=[DataRequired(), Length(max=150)],)
#
#     row = IntegerField('Кол-во рядов:', id='row', name='row', validators=[DataRequired(), NumberRange(min=0)],)
#     seat = IntegerField('Кол-во мест:', id='seat', name='seat', validators=[DataRequired(), NumberRange(min=0)],
#                         default=15, )
#     recommendedDonation = IntegerField('Рекомендованный донат:', id='recommendedDonation', name='recommendedDonation',
#                                        validators=[DataRequired(), NumberRange(min=0, max=5000)], default=300, )
#
#     # startDateTime = FieldList(
#     #     DateTimeLocalField('Дата и время начала:', validators=[DataRequired()], format='%Y-%m-%dT%H:%M',
#     #                        default=datetime(year=2023, month=5, day=14, hour=15)),
#     #     min_entries=1)
#     startDateTime = DateTimeLocalField('Дата и время начала:', id='startDateTime', name='startDateTime',
#                                        validators=[DataRequired()], format='%Y-%m-%dT%H:%M',
#                                        default=datetime(year=2023, month=5, day=14, hour=15))
#
#     # endDateTime = FieldList(
#     #     DateTimeLocalField('Дата и время окончания:', validators=[DataRequired()], format='%Y-%m-%dT%H:%M',
#     #                        default=datetime(year=2023, month=5, day=13, hour=15)),
#     #     min_entries=1)
#
#     endDateTime = DateTimeLocalField('Дата и время окончания:', id='endDateTime', name='endDateTime',
#                                      validators=[DataRequired()], format='%Y-%m-%dT%H:%M',
#                                      default=datetime(year=2023, month=5, day=13, hour=15))
#
#     submit = SubmitField('Создать мероприятие', id='submit')
#
#     def validate_countOfMembers(form, field):
#         min_count = 1
#         max_count = 100
#         if field.data < min_count:
#             raise ValidationError(f'Минимальное кол-во участников: {min_count}')
#         if field.data > max_count:
#             raise ValidationError(f'Максимальное кол-во участников: {max_count}')
#
#     def validate_expectedAmount(form, field):
#         min_amount = 0
#         max_amount = 500000
#         if field.data < min_amount:
#             raise ValidationError(f'Минимальная сумма для сбора: {min_amount}')
#         if field.data > max_amount:
#             raise ValidationError(f'Максимальная сумма для сбора: {max_amount}')
#
#     # def validate_endDateTime(self, field):
#     #     for i, end_time in enumerate(field.data):
#     #         if field.data[i] <= self.startDateTime.data[i]:
#     #             raise ValidationError(
#     #                 f'Дата и время окончания должны быть позже даты и времени начала (для записи {i + 1})')
#     #             # f'Дата и время окончания должны быть позже даты и времени начала')
#     def validate_endDateTime(self, field):
#         if field.data <= self.startDateTime.data:
#             raise ValidationError(
#                 f'Дата и время окончания должны быть позже даты и времени начала')
#
#
# TODO: edit позже
# class PersonalSettingsForm(FlaskForm):
#     firstName = StringField('Имя:', validators=[DataRequired(), Length(max=50)], default="Квартирник от Сали")
#     lastName = StringField('Фамилия:', validators=[DataRequired(), Length(max=50)], default="Квартирник от Сали")
#     middleName = StringField('Отчество:', validators=[DataRequired(), Length(max=90)], default="Квартирник от Сали")
#     birthday = DateField('Дата рождения:', validators=[DataRequired()], default=date(year=2000, month=5, day=14))
#
#     submit = SubmitField('Сохранить изменения', id='submit')

# TODO: edit event позже
# class OrganizerSettingsForm(FlaskForm):
#     def validate_cardNumber(form, field):
#         if field.data and not field.data.isdigit():
#             raise ValidationError('Поле должно содержать только цифры')
#
#     name = StringField('Имя:', name='name', validators=[DataRequired(), Length(max=150)], description='Эль Примо')
#
#     description = TextAreaField('Описание:', name='description', validators=[Length(max=800)],
#                                 description='Напишите что-то об организации (о себе)...')
#
#     cardNumber = StringField('Номер банковской карты:', name='cardNumber', validators=[DataRequired(), Length(min=16, max=16)],
#                              description='1111222233334444')
#
#     cardHolderName = StringField('Владелец карты:', name='cardHolderName', validators=[DataRequired()], description='ФИО владельца карты')
#     vk = StringField('VK:', name='vk', validators=[Length(max=200)], description='Макс. длина - 200')
#     telegram = StringField('Telegram:', name='telegram', validators=[Length(max=200)], description='Макс. длина - 200')
#     instagram = StringField('Instagram:', name='instagram', validators=[Length(max=200)], description='Макс. длина - 200')
#     facebook = StringField('Facebook:', name='facebook', validators=[Length(max=200)], description='Макс. длина - 200')
#     twitter = StringField('Twitter:', name='twitter', validators=[Length(max=200)], description='Макс. длина - 200')
#
#     submit = SubmitField('Сохранить изменения', id='submit')


class ChangePassword(FlaskForm):
    def validate_repeatPassword(self, field):
        if field.data != self.newPassword.data:
            raise ValidationError('Пароли не совпадают')

    # TODO: тоже поменять на PasswordField
    currentPassword = StringField(
        'Текущий пароль:', id='currentPassword', name='currentPassword',
        validators=[DataRequired(), Length(min=6, max=36)],
        description='example123', default='string')

    newPassword = StringField(
        'Новый пароль:', id='newPassword', name='newPassword', validators=[DataRequired(), Length(min=6, max=36)],
        description='example123', default='string')

    repeatPassword = StringField(
        'Подтверждение пароля:', id='repeatPassword', name='repeatPassword',
        validators=[DataRequired(), Length(min=6, max=36)],
        description='example123', default='string')

    submit = SubmitField('Изменить')


class ChangeEmail(FlaskForm):
    email = EmailField(
        'E-mail:', id='email', name='email', validators=[DataRequired()],
        description='example@mail.ru', default='ernest@mail.ru')

    submit = SubmitField('Изменить')


class OrganizerCreateForm(FlaskForm):
    def validate_cardNumber(form, field):
        if field.data and not field.data.isdigit():
            raise ValidationError('Поле должно содержать только цифры')

    name = StringField('Имя:', validators=[DataRequired(), Length(max=150)], default="МАЕРЗ", description='Эль Примо')

    description = TextAreaField('Описание:', validators=[Length(max=800)], default='Я ТУТ САМЫЙ КРУТОЙ',
                                description='Напишите что-то об организации (о себе)...')

    cardNumber = StringField('Номер банковской карты:', validators=[DataRequired(), Length(min=16, max=16)],
                             default="0000111122223333", description='1111222233334444')

    cardHolderName = StringField('Владелец карты:', validators=[DataRequired()], default="ИВАНОВ И. И.",
                                 description='ФИО владельца карты')

    vk = StringField('VK:', validators=[Length(max=200)], description='Макс. длина - 200')
    telegram = StringField('Telegram:', validators=[Length(max=200)], description='Макс. длина - 200')
    instagram = StringField('Instagram:', validators=[Length(max=200)], description='Макс. длина - 200')
    facebook = StringField('Facebook:', validators=[Length(max=200)], description='Макс. длина - 200')
    twitter = StringField('Twitter:', validators=[Length(max=200)], description='Макс. длина - 200')

    submit = SubmitField('Создать организатора', id='submit')
