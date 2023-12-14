$('form').submit(function (event) {
    event.preventDefault(); // Отменяем стандартное поведение формы
    const formData = $(this).serialize(); // Сериализуем данные формы
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'), // Отправляем запрос на URL, указанный в атрибуте "action"
        data: formData,
        success: function (data) {
            // После успешного выполнения запроса обновляем поля на странице
            $('#name').val(data['name']);
            $('#description').val(data['description']);
            $('#expectedAmount').val(data['expectedAmount']);
            $('#validateStatus').val(data['validateStatus']);
            $('#countOfMembers').val(data['countOfMembers']);
            $('#concession').val(data['concession']);
            $('#categoryId').val(data['categoryId']);
            $('#organizerId').val(data['organizerId']);
            $('#startDateTime').val(data['startDateTime']);
            $('#endDateTime').val(data['endDateTime']);
            $('#venueName').val(data['venueName']);
            $('#venueDescription').val(data['venueDescription']);
            $('#address').val(data['address']);
            $('#country').val(data['country']);
            $('#state').val(data['state']);
            $('#city').val(data['city']);
            $('#ticketType').val(data['ticketType']);
            $('#row').val(data['row']);
            $('#seat').val(data['seat']);
            $('#recommendedDonation').val(data['recommendedDonation']);
        },
        error: function () {
            alert('Ошибка отправки данных');
        }
    });
});