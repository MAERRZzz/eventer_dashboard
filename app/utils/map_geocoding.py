# from flask import request, jsonify
# import requests
#
#
# def venue_info(data):
#     venueData = request.get_json()
#     latitude = venueData['latitude']
#     longitude = venueData['longitude']
#
#     # Вызов OpenStreetMap API для получения адреса и названия места
#     url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}'
#     response = requests.get(url).json()
#
#     address = response['displayName']
#     venueName = response.get('poi', '') or response.get('address', '')
#
#     print(venueName, address)
#
#     # Возвращение данных о месте в формате JSON
#     return jsonify({
#         'address': address,
#         'venueName': venueName
#     })
#
#     # lat = data['lat']
#     # lng = data['lng']
#
#     # Обработка координат
#
#     # print(lat, lng)
