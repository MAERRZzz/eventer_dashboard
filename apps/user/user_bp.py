from flask import request, render_template, Blueprint, flash, redirect
from apps.config import Endpoint, FlashMessage, FlashCategory, Method
from utils.api_requests import request_api
from utils.imgur import upload_image
from utils.login_required import login_required

user_bp = Blueprint('user', __name__, url_prefix='/user', template_folder='templates',
                    static_folder='static')


@user_bp.route('/settings/<int:id>', methods=['GET', 'POST'])
@login_required
def personal_edit(id):
    user_info = request_api(Method.GET, Endpoint.USER_EP + str(id))
    user_organizers = [organizer for organizer in user_info['organizers']]

    user_email = f"{user_info['email'][0]}**@" \
                 f"{user_info['email'][user_info['email'].find('@') + 1]}**" \
                 f"{user_info['email'][user_info['email'].rfind('.'):]}"

    if request.method == "POST":
        avatar = user_info['avatar']
        print(request.files.get('avatar'))

        if request.files.get('avatar'):
            print('sssssssssssssssss\n\n')
            avatar = upload_image(request.files['avatar'].read())

        data = {
            "firstName": request.form.get('firstName'),
            "lastName": request.form.get('lastName'),
            "middleName": request.form.get('middleName'),
            "birthday": request.form.get('birthday'),
            "avatar": avatar,
        }
        try:
            request_api(Method.PUT, Endpoint.USER_EP + str(id), data=data)
            flash(FlashMessage.SUCCESS_EDIT, FlashCategory.SUCCESS)

            return redirect(f'/user/settings/{id}')

        except Exception as error:
            print(f"Ошибка (setting_bp): {error}")

    return render_template(
        'user_settings.html',
        user_info=user_info,
        user_email=user_email,
        user_organizers=user_organizers
    )
