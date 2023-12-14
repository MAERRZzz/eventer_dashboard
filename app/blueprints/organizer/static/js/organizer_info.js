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
            $('#cardNumber').val(data['cardNumber']);
            $('#cardHolderName').val(data['cardHolderName']);
            $('#facebook').val(data['facebook']);
            $('#telegram').val(data['telegram']);
            $('#vk').val(data['vk']);
            $('#twitter').val(data['twitter']);
            $('#instagram').val(data['instagram']);
        },
        error: function () {
            alert('Ошибка отправки данных');
        }
    });
});