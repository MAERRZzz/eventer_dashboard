from pprint import pprint

from flask import request, render_template, session, redirect, Blueprint, flash, jsonify
from app.config import Endpoint, Method, FlashMessage, FlashCategory, DefaultImage
from app.utils.api_requests import request_api
from app.utils.forms_validate import EventCreateForm
from app.utils.imgur import upload_image, upload_edit
from app.utils.login_required import login_required
import traceback

# from app.utils.map_geocoding import venue_info

event_bp = Blueprint('event', __name__, url_prefix='/event', template_folder='templates', static_folder='static')


@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def event_create():
    user_info = request_api(Method.GET, Endpoint.USER_EP + session['userId'])
    user_organizers = []
    for organizer in user_info['organizers']:
        user_organizers.append(organizer)

    # Список категорий
    genres = request_api(Method.GET, Endpoint.GENRE_EP)

    form = EventCreateForm()
    if form.validate_on_submit():
        photos = [DefaultImage.venue]
        venuePhoto = request.files.get('photos')
        if venuePhoto:
            photos.append(upload_image(venuePhoto.read()))
        data = {
            "name": form.name.data,
            "description": form.description.data,
            "expectedAmount": form.expectedAmount.data,
            "recommendedDonation": form.recommendedDonation.data,
            "validateStatus": request.form.get('validateStatus'),
            "countOfMembers": form.countOfMembers.data,
            "status": "ACTIVE",
            "concession": form.concession.data,
            "genreId": request.form.get('genreId'),
            "organizerId": request.form.get('organizerId'),
            "eventDateTimes": [
                {
                    "startDateTime": str(form.startDateTime.data),
                    "endDateTime": str(form.endDateTime.data),
                }
            ],
            "venues": [
                {
                    "name": form.venueName.data,
                    "description": form.venueDescription.data,
                    "photos": photos,
                    "address": form.address.data,
                    "seats": form.seats.data,
                    "country": form.country.data,
                    "state": form.state.data,
                    "city": form.city.data,
                }
            ]
        }

        try:
            request_api(Method.POST, Endpoint.EVENT_EP, data=data)
        except Exception as error:
            traceback.print_exc()
            print("Ошибка (event_bp.py):", str(error))
            return redirect('/login')

        return redirect('/')

    return render_template('event_create.html', form=form, user_organizers=user_organizers,
                           user_info=user_info, genres=genres)


@event_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event_info = request_api(Method.GET, Endpoint.EVENT_EP + str(id))

    user_info = request_api(Method.GET, Endpoint.USER_EP + session['userId'])
    user_organizers = []
    for organizer in user_info['organizers']:
        user_organizers.append(organizer)

    # Список категорий
    genres = request_api(Method.GET, Endpoint.GENRE_EP)

    # form = EventEditForm()
    # if form.validate_on_submit():
    if request.method == "POST":
        venuePhoto = request.files.get('photos')
        if venuePhoto:
            upload_edit(id, venuePhoto.read(), venue=True)
        else:
            data = {
                "name": request.form.get('name'),
                "description": request.form.get('description'),
                "expectedAmount": request.form.get('expectedAmount'),
                "recommendedDonation": request.form.get('recommendedDonation'),
                "validateStatus": request.form.get('validateStatus'),
                "countOfMembers": request.form.get('countOfMembers'),
                # "status": "ACTIVE",  # Кнопка в html, которая может отменить/отложить
                "concession": request.form.get('concession'),
                "genreId": request.form.get('genreId'),
                "organizerId": request.form.get('organizerId'),
                "eventDateTimes": [
                    {
                        "startDateTime": str(request.form.get('startDateTime'),),
                        "endDateTime": str(request.form.get('endDateTime'),),
                    }
                ],
                "venues": [
                    {
                        "name": request.form.get('venueName'),
                        "description": request.form.get('venueDescription'),
                        "address": request.form.get('address'),
                        "seats": request.form.get('seats'),
                        "country": request.form.get('country'),
                        "state": request.form.get('state'),
                        "city": request.form.get('city'),
                    }
                ]
            }
            try:
                request_api(Method.PUT, Endpoint.EVENT_EP + str(id), data=data)

                flash(FlashMessage.SUCCESS_EDIT, FlashCategory.SUCCESS)
                event_info = request_api(Method.GET, Endpoint.EVENT_EP + str(id))

            except Exception as error:
                traceback.print_exc()
                print("Ошибка (event_bp.py):", str(error))
                return redirect(f'/event/edit/{id}')

    return render_template('event_edit.html', id=id, user_info=user_info, event_info=event_info,
                           user_organizers=user_organizers, genres=genres)


@event_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_event(id):
    try:
        request_api(Method.DELETE, Endpoint.EVENT_EP + str(id))

        flash(FlashMessage.SUCCESS_EDIT, FlashCategory.SUCCESS)
        redirect('/')

    except Exception as error:
        traceback.print_exc()
        print("Ошибка (event_bp.py):", str(error))
