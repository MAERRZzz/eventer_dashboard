from functools import wraps

from flask import session, flash, redirect

from apps.config import FlashMessage, FlashCategory
from utils.jwt_extension import token_expired, refresh_token


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('accessToken'):
            flash(FlashMessage.UNAUTHORIZED, FlashCategory.INFO)
            return redirect('/login')

        if token_expired(session['accessToken']):
            if session.get('refreshToken'):
                if token_expired(session['refreshToken']):
                    flash(FlashMessage.EXPIRED_SESSION, FlashCategory.INFO)
                    return redirect('/login')
                else:
                    refresh_token()
            else:
                del session['accessToken']
                flash(FlashMessage.EXPIRED_SESSION, FlashCategory.INFO)
                return redirect('/login')

        return f(*args, **kwargs)

    return decorated_function
