if (document.getElementById('avatarImage')){
document.getElementById('avatarImage').addEventListener('change', handleImageChange('avatarImage'));
}
if (document.getElementById('backgroundImage')){
document.getElementById('backgroundImage').addEventListener('change', handleImageChange('backgroundImage'));
}
if (document.getElementById('venueImage')){
document.getElementById('venueImage').addEventListener('change', handleImageChange('venueImage'));
}


function handleImageChange(elementId) {

    let cropper = null; // Сохраняем ссылку на экземпляр Cropper
    return function (e) {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = function (event) {
            const img = document.getElementById(elementId + 'Edit');
            img.src = event.target.result;

            let aspectRatio = 1; // значение по умолчанию

            if (elementId === 'backgroundImage') {
                aspectRatio = 16 / 9;
            } else if (elementId === 'venueImage') {
                aspectRatio = 16 / 9;
            }

            // Удаление предыдущего экземпляра Cropper, если он существует
            if (cropper) {
                cropper.destroy();
            }

            cropper = new Cropper(img, {
                aspectRatio: aspectRatio,
                viewMode: 1,
                autoCropArea: 100,
                cropBoxResizable: true,
                zoomable: false,
            });



            // Обработчик события для кнопки сохранения
            const saveButton = document.getElementById(elementId + 'Submit');
            saveButton.addEventListener('click', function () {

                const canvas = cropper.getCroppedCanvas();
                canvas.toBlob(function (blob) {
                    const fileName = file.name;
                    const inputField = document.getElementById(elementId).name;

                    const formData = new FormData();
                    formData.append(inputField, blob, fileName)

                    if (window.location.href.includes('event')) {
                        formData.append('name', document.getElementById('name').value);
                        formData.append('description', document.getElementById('description').value);
                        formData.append('expectedAmount', document.getElementById('expectedAmount').value);
                        formData.append('validateStatus', document.getElementById('validateStatus').value);
                        formData.append('countOfMembers', document.getElementById('countOfMembers').value);
                        formData.append('status', document.getElementById('status').value);
                        formData.append('concession', document.getElementById('concession').value);
                        formData.append('categoryId', document.getElementById('categoryId').value);
                        formData.append('organizerId', document.getElementById('organizerId').value);
                        formData.append('startDateTime', document.getElementById('startDateTime').value);
                        formData.append('endDateTime', document.getElementById('endDateTime').value);
                        formData.append('venueName', document.getElementById('venueName').value);
                        formData.append('venueDescription', document.getElementById('venueDescription').value);
                        formData.append('address', document.getElementById('address').value);
                        formData.append('country', document.getElementById('country').value);
                        formData.append('state', document.getElementById('state').value);
                        formData.append('city', document.getElementById('city').value);
                        formData.append('ticketType', document.getElementById('ticketType').value);
                        formData.append('row', document.getElementById('row').value);
                        formData.append('seat', document.getElementById('seat').value);
                        formData.append('recommendedDonation', document.getElementById('recommendedDonation').value);
                    }

                    // Отправка файла на сервер с помощью Fetch API
                    fetch(window.location.href, {
                        method: 'POST',
                        body: formData
                    })
                        .then(response => response.text())
                        .then(data => {
                            console.log('Ответ сервера:', data);
                            // Обработка ответа от сервера
                            // ...
                        })
                        .catch(error => {
                            console.error('Ошибка:', error);
                            // Обработка ошибки
                            // ...
                        });
                }, 'image/jpeg');
            });
        };

        reader.readAsDataURL(file);
    };

}
