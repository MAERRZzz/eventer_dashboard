from flask import flash, request, render_template, session, redirect, Blueprint

from app.utils.api_requests import request_api
from app.config import Endpoint, FlashMessage, FlashCategory, Method
from app.utils.forms_validate import LoginForm
import traceback
import jwt

login_bp = Blueprint('login', __name__, url_prefix='/login', template_folder='templates', static_folder='static')


@login_bp.route('', methods=['GET', 'POST'])
def login():
    if request.referrer != request.url_root + 'login/':
        session['request'] = request.referrer
    if session.get('accessToken'):
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        data = {
            "email": f"{form.email.data}",
            "password": f"{form.password.data}"
        }
        response_json = request_api(Method.POST, Endpoint.AUTH_LOGIN_EP, data=data)

        try:
            session['userId'] = str(jwt.decode(response_json['accessToken'], options={"verify_signature": False})['sub']['userId'])
            session['roleId'] = str(jwt.decode(response_json['accessToken'], options={"verify_signature": False})['sub']['roleId'])
            session['accessToken'] = response_json['accessToken']

            print(form.rememberMe.data)
            if form.rememberMe.data:
                session['refreshToken'] = response_json['refreshToken']
            if session.get('request'):
                return redirect(session['request'])
            else:
                return redirect('/')

        except Exception as error:
            if response_json.get('message') == "User not found":
                flash(FlashMessage.USER_NOT_FOUND, FlashCategory.DANGER)
            else:
                traceback.print_exc()
                print("Ошибка (login_bp):", str(error))
                flash(FlashMessage.LOGIN_ERROR, FlashCategory.DANGER)

    return render_template('login.html', form=form)
