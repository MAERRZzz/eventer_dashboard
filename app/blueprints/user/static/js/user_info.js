$('form').submit(function (event) {
    event.preventDefault(); // Отменяем стандартное поведение формы
    const formData = $(this).serialize(); // Сериализуем данные формы
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'), // Отправляем запрос на URL, указанный в атрибуте "action"
        data: formData,
        success: function (data) {
            // После успешного выполнения запроса обновляем поля на странице
            $('#firstName').val(data['lastName']);
            $('#lastName').val(data['firstName']);
            $('#middleName').val(data['firstName']);
            $('#birthday').val(data['firstName']);
            $('#avatar').val(data['firstName']);
        },
        error: function () {
            alert('Ошибка отправки данных   ');
        }
    });
});