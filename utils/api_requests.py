from flask import session, current_app, flash
from requests.api import request
import json
from apps.config import Config, FlashMessage, FlashCategory


# Функция-шаблон для запросов на API
def request_api(method, endpoint, data=None, params=None):
    headers = {'Authorization': f"Bearer {session.get('accessToken')}", "Content-Type": "application/json"}
    if data:
        data = json.dumps(data)
    response = request(method, Config.API_URL + endpoint, headers=headers, data=data, params=params)

    current_app.logger.info(f"{response.request.method} {endpoint} - {response.status_code}, {data=}, {params=}")

    try:
        if response.status_code == 200:
            response_json = response.json()
            return response_json

        if response.status_code == 201:
            response_json = response.json()
            return response_json

        elif response.status_code == 204:
            pass
    except Exception as error:
        current_app.logger.error("ОШИБКА:", response.url, '-', response.status_code, '\n\n', error)
