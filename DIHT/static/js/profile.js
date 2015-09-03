$(function() {
    function view_modal_errors(form, request){
        errors = JSON.parse(request.responseText);
        $('.errorlist').remove();
        for (var k in errors)
            form.find('#id_'+k).after('<ul class="errorlist"><li>' + errors[k] + '</li></ul>');
    }

    $('#form-modal').on('submit', '.profile-form,.add-money-form,.remove-money-form', function (ev) {
        ev.preventDefault();
        var form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data) {
                $("#form-modal").modal('hide');
                window.location.reload();
            },
            error: function(request, status, error) {
                view_modal_errors(form, request)
            }
        });
        return false;
    });
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

