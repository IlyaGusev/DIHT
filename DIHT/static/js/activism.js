$(function() {
    function view_modal_errors(form, request){
        errors = JSON.parse(request.responseText);
        $('.errorlist').remove();
        for (var k in errors)
            form.find('#id_'+k).after('<ul class="errorlist"><li>' + errors[k] + '</li></ul>');
    }
    $('#form-modal').on('submit', '.task-create-form,.event-create-form', function() {
        var form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(response) {
                $("#form-modal").modal('hide');
                window.location.replace(response.url)
            },
            error: function(request, status, error) {
                view_modal_errors(form, request)
            }
        });
        return false;
    });
});