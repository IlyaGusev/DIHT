$(function() {
    // Загрузка аватарки
    $('#fileinput').on('change', function(event){
        var file = $('#fileinput').prop('files')[0];
        var data = new FormData();
        data.append("img", file);
        console.log(file)
        $.ajax({
            url: $('input[type=file]').attr('href'),
            type: 'POST',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(data, textStatus, jqXHR){
                window.location.reload();
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log('ERRORS: ' + textStatus);
            }
        });
        return false;
    });
});

