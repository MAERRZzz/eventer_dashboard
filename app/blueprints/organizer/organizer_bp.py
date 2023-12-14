from flask import request, render_template, Blueprint, flash, session, redirect
from app.config import Endpoint, FlashMessage, FlashCategory, Method, DefaultImage
from app.utils.api_requests import request_api
from app.utils.forms_validate import OrganizerCreateForm
from app.utils.imgur import upload_edit, upload_image
from app.utils.login_required import login_required

organizer_bp = Blueprint('organizer', __name__, url_prefix='/organizer', template_folder='templates',
                         static_folder='static')


@organizer_bp.route('/create', methods=['GET', 'POST'])
@login_required
def organizer_create():
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
            "instagram": form.instagram.data,
            "userId": session['userId']
        }
        request_api(Method.POST, Endpoint.ORGANIZER_EP, data=data)

        flash(FlashMessage.SUCCESS_ORGANIZER_CREATE, FlashCategory.SUCCESS)
        return redirect('/')

    return render_template('organizer_create.html', form=form, default_logo=DefaultImage.avatar,
                           default_background=DefaultImage.background)


@organizer_bp.route('/settings/<int:id>', methods=['GET', 'POST'])
@login_required
def organizer_settings(id):
    organizer_info = request_api(Method.GET, Endpoint.ORGANIZER_EP + str(id))

    if request.method == "POST":
        logo = request.files.get('logo')
        background = request.files.get('background')
        if logo:
            upload_edit(id, logo.read(), logo=True)
        elif background:
            upload_edit(id, background.read(), background=True)
        else:
            data = {
                "name": request.form.get('name'),
                "description": request.form.get('description'),
                "cardNumber": request.form.get('cardNumber'),
                "cardHolderName": request.form.get('cardHolderName'),
                "facebook": request.form.get('facebook'),
                "telegram": request.form.get('telegram'),
                "vk": request.form.get('vk'),
                "twitter": request.form.get('twitter'),
                "instagram": request.form.get('instagram'),
            }
            try:
                request_api(Method.PUT, Endpoint.ORGANIZER_EP + str(id), data=data)

                flash(FlashMessage.SUCCESS_EDIT, FlashCategory.SUCCESS)
                organizer_info = request_api(Method.GET,
                                             Endpoint.ORGANIZER_EP + str(id))  # Обновленные данные
                print(organizer_info)
            except Exception as error:
                print(f"Ошибка (setting_bp): {error}")

    return render_template('organizer_settings.html', organizer_info=organizer_info, id=id)
