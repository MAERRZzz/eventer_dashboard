from flask import session
from requests.api import request
import json
from app.config import Config


# Функция-шаблон для запросов на API
def request_api(method, endpoint, data=None, params=None):
    headers = {'Authorization': f"Bearer {session.get('accessToken')}", "Content-Type": "application/json"}
    if data:
        data = json.dumps(data)
    response = request(method, Config.API_URL + endpoint, headers=headers, data=data, params=params)
    print(f"{response.url, response.request}--{response.status_code} - {data=} - {params=}")
    response_json = response.json()
    try:
        if response.status_code == 200 or 201:
            return response_json
        elif response.status_code == 204:
            pass
    except Exception as error:
        print("ОШИБКА:", response.url, '-', response.status_code, '\n\n', error)
