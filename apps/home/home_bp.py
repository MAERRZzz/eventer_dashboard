from datetime import datetime
import locale
from pprint import pprint

from flask import render_template, session, Blueprint, current_app, flash
from utils.api_requests import request_api
from apps.config import Endpoint, Method, Config, FlashCategory
from utils.login_required import login_required

home_bp = Blueprint('home', __name__, template_folder='templates', static_folder='static/assets/')


@home_bp.route('/', methods=['GET', 'POST'])
@login_required
def my_events():
    current_app.logger.info(f"\nBearer {session['accessToken']}\nBase-url: {Config.API_URL}")

    user_info = request_api(Method.GET, Endpoint.USER_EP + session.get('userId'))
    pprint(user_info)
    print(session.get('accessToken'))

    user_organizers = [organizer for organizer in user_info['organizers']]

    organizer_events = []
    for organizer in user_organizers:
        events = request_api(Method.GET, Endpoint.EVENT_EP, params={'organizerId': organizer['id']})

        if events:
            for i, event in enumerate(events):
                bookings = request_api(Method.GET, Endpoint.BOOKING_EP, params={'eventId': event['id']})

                events[i]['bookings'] = bookings

                event_donations = request_api(Method.GET, Endpoint.EVENT_DONATION_EP,
                                              params={'eventId': event['id']})

                result = {}
                for item in event_donations:
                    user_id = item['user']['id']
                    amount = item['amount']
                    if user_id in result:
                        result[user_id]['total_amount'] += amount
                    else:
                        result[user_id] = {
                            'user': item['user'],
                            'total_amount': amount
                        }

                events[i]['event_donations'] = list(result.values())

                total_amount = sum(donation['amount'] for donation in event_donations)
                events[i]['total_amount'] = total_amount
                events[i]['total_percent'] = total_amount * 100 / events[i]['expectedAmount']

            organizer_events += events

    for event in organizer_events:
        locale.setlocale(locale.LC_TIME, 'ru_RU')
        event['eventDates'][0]['startDateTime'] = (
            datetime.strptime(event['eventDates'][0]['startDateTime'], "%Y-%m-%dT%H:%M:%S")).strftime(
            "%B %d, %H:%M")
        event['eventDates'][0]['endDateTime'] = (
            datetime.strptime(event['eventDates'][0]['endDateTime'], "%Y-%m-%dT%H:%M:%S")).strftime(
            "%B %d, %H:%M")

    return render_template('home.html', user_info=user_info,
                           organizer_events=organizer_events,
                           user_organizers=user_organizers)
