from flask import session, redirect, Blueprint

logout_bp = Blueprint('logout', __name__, url_prefix='/logout')


@logout_bp.route('/', methods=['GET', 'POST'])
def logout():
    if session.get('accessToken'):
        del session['accessToken']

    if session.get('refreshToken'):
        del session['refreshToken']

    return redirect('/login')
