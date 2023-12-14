from flask import flash, render_template, session, redirect, Blueprint

from app.utils.api_requests import request_api
from app.config import Endpoint, FlashMessage, FlashCategory, Method, DefaultImage
from app.utils.forms_validate import RegistrationForm

from dotenv import load_dotenv

load_dotenv()
registration_bp = Blueprint('registration', __name__, url_prefix='/registration', template_folder='templates',
                            static_folder='static')


@registration_bp.route('', methods=['GET', 'POST'])
def registration():
    if session.get('accessToken'):
        return redirect('/')

    form = RegistrationForm()
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

        if response.get('message') == 'Email exists':
            form.email.errors.append('Этот email уже занят')
        else:
            flash(FlashMessage.SUCCESS_REGISTRATION, FlashCategory.SUCCESS)
            return redirect('/login')

    return render_template('registration.html', form=form)
