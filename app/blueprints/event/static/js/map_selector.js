// // Создаем переменную для хранения координат выбранного места
// var selectedCoordinates = null;
//
// var map = L.map('map').setView([44.9521, 34.1024], 12);
// var marker;
//
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
//     maxZoom: 19
// }).addTo(map);
//
// map.on('click', function (event) {
//     var position = event.latlng;
//
//     // Удаление предыдущей метки, если она существует
//     if (marker) {
//         map.removeLayer(marker);
//     }
//
//     marker = L.marker(position, {
//         draggable: true
//     }).addTo(map);
//
//   marker.on('dragend', function(event) {
//     var marker = event.target;
//     var position = marker.getLatLng();
//     var placeData = {
//       latitude: position.lat,
//       longitude: position.lng
//     };
//
//     // Обновляем переменную с координатами выбранного места
//     selectedCoordinates = placeData;
//     console.log(placeData);
//   });
// });
//
// // Функция, которая будет вызываться при нажатии на кнопку "Отправить"
// function sendData() {
//   // Проверяем, что координаты выбранного места были сохранены
//   if (selectedCoordinates) {
//     // Отправляем координаты на сервер с помощью AJAX-запроса
//     var xhr = new XMLHttpRequest();
//     xhr.open('POST', '/event/create', true);
//     xhr.setRequestHeader('Content-Type', 'application/json');
//     xhr.onreadystatechange = function() {
//       if (xhr.readyState === 4 && xhr.status === 200) {
//         // Обработка успешного ответа от сервера
//         console.log('Координаты успешно отправлены!');
//       }
//     };
//     xhr.send(JSON.stringify(selectedCoordinates));
//   } else {
//     console.log('Выберите место на карте перед отправкой!');
//   }
// }
