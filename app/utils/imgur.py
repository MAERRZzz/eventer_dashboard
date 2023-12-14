from flask import flash
from app.config import FlashMessage, FlashCategory, Method, Endpoint
import requests

from dotenv import load_dotenv
import os

from app.utils.api_requests import request_api

load_dotenv()


def upload_image(image):
    image_url = upload_request(image)
    if image_url:
        print(f"Изображение загружено\n{image_url}")
        return image_url
    else:
        return flash(FlashMessage.UPLOAD_IMAGE_ERROR, FlashCategory.DANGER)


def upload_edit(id, image, avatar=False, logo=False, background=False, venue=False):
    image_url = upload_request(image)
    if image_url:
        data = {}
        if avatar:
            data = {"avatar": image_url}
            request_api(Method.PUT, Endpoint.USER_EP + str(id), data=data)
            flash(FlashMessage.SUCCESS_EDIT, FlashCategory.SUCCESS)

            print(f"Изображение :{image_url}")
        # TODO: проверить норм ли работает редактирования ивента
        elif venue:
            data = {"venues": [{"photos": [image_url]}]}
            request_api(Method.PUT, Endpoint.EVENT_EP + str(id), data=data)
            flash(FlashMessage.SUCCESS_EDIT, FlashCategory.SUCCESS)

            print(f"Изображение :{image_url}")

        else:
            if logo:
                data = {"logo": image_url}
            if background:
                data = {"background": image_url}
            request_api(Method.PUT, Endpoint.ORGANIZER_EP + str(id), data=data)
            flash(FlashMessage.SUCCESS_EDIT, FlashCategory.SUCCESS)

            print(f"Изображение :{image_url}")
    else:
        return flash(FlashMessage.UPLOAD_IMAGE_ERROR, FlashCategory.DANGER)


def upload_request(image):
    endpoint = 'https://api.imgur.com/3/upload'
    headers = {'Authorization': f'Client-ID {os.getenv("IMGUR_CLIENT_ID")}'}
    image = {'image': image}

    response = requests.post(endpoint, headers=headers, files=image)
    response_json = response.json()
    print(response_json)

    if response.status_code == 200 and response_json['success']:
        imgur_url = response_json['data']['link']
        print(f"Image ID - {response_json['data']['id']}")
        return imgur_url
    else:
        return None
