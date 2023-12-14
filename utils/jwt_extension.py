from flask import session
import jwt
import requests
from datetime import datetime

from apps import Config
from apps.config import Endpoint


def token_expired(token):
    try:
        token_exp = jwt.decode(token, options={"verify_signature": False})['exp']
        if token_exp > datetime.now().timestamp():
            return False
        else:
            return True
    except Exception as error:
        print(f"Ошибка (jwt_extension): {error}")


def refresh_token():
    headers = {'Authorization': f"Bearer {session['refreshToken']}", "Content-Type": "application/json"}
    response = requests.post(Config.API_URL + Endpoint.AUTH_REFRESH_TOKEN_EP, headers=headers)
    response_json = response.json()

    print(f"{Endpoint.AUTH_REFRESH_TOKEN_EP} - Status: {response.status_code}\n")

    session['accessToken'] = response_json['accessToken']
    session['refreshToken'] = response_json['refreshToken']
