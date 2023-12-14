from datetime import datetime

from flask import render_template, session, redirect, Blueprint, flash
from app.utils.api_requests import request_api
from app.config import Endpoint, Method, FlashCategory
from app.utils.login_required import login_required

from dotenv import load_dotenv
import os

load_dotenv()

home_bp = Blueprint('home', __name__, template_folder='templates', static_folder='static/assets/')


@home_bp.route('/', methods=['GET', 'POST'])
@login_required
def my_events():
    try:
        print(f"--------\nBearer {session['accessToken']}\n--------")
        print(os.getenv('API_URL'), '\n--------')
        user_info = request_api(Method.GET, Endpoint.USER_EP + session.get('userId'))

        if len(user_info['organizers']) > 0:
            organizer_events = []
            user_organizers = []
            for organizer in user_info['organizers']:
                user_organizers.append(organizer)
                events = request_api(Method.GET, Endpoint.EVENT_EP, params={'organizerId': organizer['id']})
                organizer_events += events

            # Преобразование дат проведения
            import locale
            for event in organizer_events:
                locale.setlocale(locale.LC_TIME, 'ru_RU')
                event['eventDates'][0]['startDateTime'] = (
                    datetime.strptime(event['eventDates'][0]['startDateTime'], "%Y-%m-%dT%H:%M:%S")).strftime(
                    "%B %d, %H:%M")
                event['eventDates'][0]['endDateTime'] = (
                    datetime.strptime(event['eventDates'][0]['endDateTime'], "%Y-%m-%dT%H:%M:%S")).strftime(
                    "%B %d, %H:%M")

            return render_template('dashboard.html', user_info=user_info, organizer_events=organizer_events,
                                   user_organizers=user_organizers)
        else:

            return render_template('dashboard.html', user_info=user_info)

    except Exception as error:
        print("Ошибка (home_bp):", str(error))
        flash('Ошибка сервера.', FlashCategory.DANGER)

        return redirect('/logout')
    # return render_template('home.html', user_info=False, organizer_events=False, user_organizers=False)
