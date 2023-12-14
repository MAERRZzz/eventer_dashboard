from flask import flash, render_template, session, redirect, Blueprint

from utils.api_requests import request_api
from apps.config import Endpoint, FlashMessage, FlashCategory, Method, DefaultImage
from utils.wtforms import LoginForm, RegisterForm
import traceback
import jwt

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='.static')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = {
            "email": f"{form.email.data}",
            "password": f"{form.password.data}"
        }
        response_json = request_api(Method.POST, Endpoint.AUTH_LOGIN_EP, data=data)

        try:
            session['userId'] = str(
                jwt.decode(response_json['accessToken'], options={"verify_signature": False})['sub']['userId'])
            session['roleId'] = str(
                jwt.decode(response_json['accessToken'], options={"verify_signature": False})['sub']['roleId'])
            session['accessToken'] = response_json['accessToken']

            if form.rememberMe.data:
                session['refreshToken'] = response_json['refreshToken']
            if session.get('request'):
                return redirect(session['request'])
            else:
                return redirect('/')

        except Exception as error:
            if response_json:
                flash(FlashMessage.USER_NOT_FOUND, FlashCategory.DANGER)
            else:
                traceback.print_exc()
                print("Ошибка (login_bp):", str(error))
                flash(FlashMessage.LOGIN_ERROR, FlashCategory.DANGER)

    return render_template('login.html', form=form)


@auth_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        data = {
            "firstName": form.firstName.data,
            "lastName": form.lastName.data,
            "middleName": form.middleName.data,
            "birthday": str(form.birthday.data),
            "password": form.password.data,
            "email": form.email.data,
            "avatar": DefaultImage.avatar,
            "trusted": True,
            "provider": "SYSTEM"
        }
        response = request_api(Method.POST, Endpoint.USER_EP, data=data)
        print(response)

        if not response:
            form.email.errors.append('Этот email уже занят')
        else:
            flash(FlashMessage.SUCCESS_REGISTRATION, FlashCategory.SUCCESS)
            return redirect('/login')

    return render_template('registration.html', form=form)


@auth_bp.route('/logout')
def logout():
    if session.get('accessToken'):
        del session['accessToken']

    if session.get('refreshToken'):
        del session['refreshToken']

    return redirect('/login')
