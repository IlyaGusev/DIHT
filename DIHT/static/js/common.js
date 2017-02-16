function view_modal_errors(form, request){
    errors = JSON.parse(request.responseText);
    $('.errorlist').remove();
    for (var k in errors)
        form.find('#id_'+k).after('<ul class="errorlist"><li>' + errors[k] + '</li></ul>');
}

function resolve_redirect(response) {
    if (response.action)
        {
            if (response.action === 'refresh')
                window.location.reload()

        } else {
            window.location.replace(response.url)
        }
}

$(function() {
    $("a[data-target=#form-modal],th[data-target=#form-modal]").click(function(ev) {
        ev.preventDefault();
        current_edit_span = $(this)[0];
        var target = $(this).attr("href");
        $("#form-modal .modal-content").load(target, function() {
             $("#form-modal").modal("show");
        });
        return false;
    });

    $('#form-modal').on('submit', '.find-form, \
                                   .password-form, \
                                   .add-points-form, \
                                   .profile-form, \
                                   .add-money-form, \
                                   .remove-money-form, \
                                   .add-payments-form, \
                                   .remove-payments-form, \
                                   .task-create-form, \
                                   .event-create-form, \
                                   .key-update-form, \
                                   .key-create-form, \
                                   .change-pass-id-form',
                                   function(ev) {
        ev.preventDefault();
        var form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(response) {
                $("#form-modal").modal('hide');
                resolve_redirect(response)
            },
            error: function(request, status, error) {
                view_modal_errors(form, request)
            }
        });
        return false;
    });

    $("body").on("click", ".delete-view", function(ev) {
        ev.preventDefault();
        var button = $(this);
        var URL = button.attr('href')
        $.ajax({type: "POST", url: URL, data: {}, dataType: "JSON"});
        window.location.reload()
    });
});
