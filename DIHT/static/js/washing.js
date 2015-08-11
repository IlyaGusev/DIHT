$(function() {
    function view_modal_errors(form, request){
        errors = JSON.parse(request.responseText);
        $('.errorlist').remove();
        for (var k in errors){
            console.log(form.find('#id_'+k))
            form.find('#id_'+k).after('<ul class="errorlist" style="color:red;"><li>' + errors[k] + '</li></ul>');
        }
    }

    $('#form-modal').on('submit', '#create-record-form,#cancel-record-form', function (ev) {
        ev.preventDefault();
        var form = $(this);
        id = $(current_edit_span)[0].id.split(" ")
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: {
                'machine' : id[0],
                'date' : id[1],
                'time_from': id[2],
                'time_to': id[3],
            },
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
    $('#form-modal').on('submit', '#block-day-form,#unblock-day-form', function (ev) {
        ev.preventDefault();
        var form = $(this);
        id = $(current_edit_span)[0].id
        var val = $("#machine_id option:selected" ).val()
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: {
                'machine': val,
                'date': id,
            },
            success: function(data) {
                $("#form-modal").modal('hide');
                window.location.reload();
            },
            error: function(request, status, error) {
                console.log(error)
            }
        });
        return false;
    });

    $("body").on("click", ".btn-open-modal", function(ev) {
        ev.preventDefault();
        current_edit_span = $(this)[0];
        id = $(current_edit_span)[0].id.split(" ")
        $("#form-modal").find(".modal-content").load($(this).attr("href"), function() {
            machine_name = $("#machine_"+id[0]).text()
            $(this).find("#create-record-body").html("<h4>Оплатить "+machine_name+" на "+id[1]+" с "+id[2]+" до "+id[3]+"</h4>")
            $(this).find("#create-record-submit").html("Оплатить ("+id[4]+' <img style="margin-top:-3px;" src="/static/img/fivt_coin_tiny_w.png">)')
            $(this).find("#cancel-record-body").html("<h4>Отказаться от записи на "+id[1]+" с "+id[2]+" до "+id[3]+"</h4>")
        });
        $("#form-modal").modal('show');
        return false;
    });
});