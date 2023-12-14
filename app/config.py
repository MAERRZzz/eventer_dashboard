import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    API_URL = os.getenv('API_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    ASSETS_ROOT = '/static/assets'


class Endpoint:
    AUTH_LOGIN_EP = 'auth/login'
    AUTH_REFRESH_TOKEN_EP = 'auth/refresh_token'

    EVENT_EP = 'event/'
    USER_EP = 'user/'
    ORGANIZER_EP = 'organizer/'
    GENRE_EP = 'genre/'


class Method:
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'


class FlashMessage:
    SUCCESS_REGISTRATION = 'Вы успешно зарегистрировались!'
    SUCCESS_ORGANIZER_CREATE = 'Организатор успешно создан!'
    SUCCESS_EDIT = 'Изменения сохранены.'
    EXPIRED_SESSION = 'Сессия истекла. Войдите снова.'
    UNAUTHORIZED = 'Авторизируйтесь для доступа к странице.'
    LOGIN_ERROR = 'Неверный e-mail или пароль.'
    USER_NOT_FOUND = 'Пользователь с такой электронной почтой не найден.'
    UPLOAD_IMAGE_ERROR = 'Не удалось загрузить изображение. Попробуйте еще раз.'


class FlashCategory:
    SUCCESS = 'success-msg'
    INFO = 'info-msg'
    DANGER = 'danger-msg'


class DefaultImage:
    avatar = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWMFZXMTRsc9uMKSKTsGQQEQ1V1qJtv7f7SVh3x66j43pMpIe3OJ-M4sfpRnbO5OyHkCM&usqp=CAU'
    background = 'https://images.unsplash.com/photo-1585314062604-1a357de8b000?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8NHx8fGVufDB8fHx8fA%3D%3D&w=1000&q=80'
    venue = 'https://www.volvogroup.com/content/dam/volvo-group/markets/master/news-and-media/1860x1050_news-and-media_upcoming-events.gif'
