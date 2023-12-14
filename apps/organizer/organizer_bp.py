from flask import request, render_template, Blueprint, flash, session, redirect, url_for
from apps.config import Endpoint, FlashMessage, FlashCategory, Method, DefaultImage
from utils.api_requests import request_api
from utils.wtforms import OrganizerCreateForm
from utils.imgur import upload_image
from utils.login_required import login_required

organizer_bp = Blueprint('organizer', __name__, url_prefix='/organizer', template_folder='templates',
                         static_folder='static')


@organizer_bp.route('/create', methods=['GET', 'POST'])
@login_required
def organizer_create():
    user_info = request_api(Method.GET, Endpoint.USER_EP + session['userId'])
    user_organizers = [organizer for organizer in user_info['organizers']]

    form = OrganizerCreateForm()
    if form.validate_on_submit():
        logo = DefaultImage.avatar
        background = DefaultImage.background
        if request.files.get('logo'):
            logo = upload_image(request.files['logo'])
        if request.files.get('background'):
            background = upload_image(request.files['background'])

        data = {
            "name": form.name.data,
            "logo": logo,
            "background": background,
            "description": form.description.data,
            "cardNumber": form.cardNumber.data,
            "cardHolderName": form.cardHolderName.data,
            "facebook": form.facebook.data,
            "telegram": form.telegram.data,
            "vk": form.vk.data,
            "twitter": form.twitter.data,
            "instagram": "none",
            "userId": session['userId']
        }
        request_api(Method.POST, Endpoint.ORGANIZER_EP, data=data)
        flash(FlashMessage.SUCCESS_ORGANIZER_CREATE, FlashCategory.SUCCESS)

        return redirect('/')

    return render_template('organizer_create.html',
                           form=form,
                           default_logo=DefaultImage.avatar,
                           default_background=DefaultImage.background,
                           user_info=user_info,
                           user_organizers=user_organizers)


@organizer_bp.route('/settings/<int:id>', methods=['GET', 'POST'])
@login_required
def organizer_settings(id):
    user_info = request_api(Method.GET, Endpoint.USER_EP + session['userId'])
    user_organizers = [organizer for organizer in user_info['organizers']]

    organizer_info = request_api(Method.GET, Endpoint.ORGANIZER_EP + str(id))

    if request.method == "POST":
        logo = organizer_info['logo']
        background = organizer_info['background']

        if request.files.get('logo'):
            logo = upload_image(request.files['logo'].read())
        if request.files.get('background'):
            background = upload_image(request.files['background'].read())

        data = {
            "name": request.form.get('name'),
            "description": request.form.get('description'),
            "logo": logo,
            "background": background,
            "cardNumber": request.form.get('cardNumber'),
            "cardHolderName": request.form.get('cardHolderName'),
            "facebook": request.form.get('facebook'),
            "telegram": request.form.get('telegram'),
            "vk": request.form.get('vk'),
            "twitter": request.form.get('twitter'),
            "instagram": "none",
        }
        try:
            request_api(Method.PUT, Endpoint.ORGANIZER_EP + str(id), data=data)
            flash(FlashMessage.SUCCESS_EDIT, FlashCategory.SUCCESS)

            return redirect(f'/organizer/settings/{id}')

        except Exception as error:
            print(f"Ошибка (setting_bp): {error}")

    return render_template('organizer_settings.html',
                           organizer_info=organizer_info,
                           id=id, user_info=user_info,
                           user_organizers=user_organizers)


@organizer_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_organizer(id):
    request_api(Method.DELETE, Endpoint.ORGANIZER_EP + str(id))

    flash(FlashMessage.ORGANIZER_DELETE, FlashCategory.INFO)
    return redirect('/')
