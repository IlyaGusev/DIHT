$(function() {
    $('#form-modal').on('submit', '.create-record-form,.cancel-record-form', function () {
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
            $(this).find("#cancel-record-body").html("<h4>Отказаться от записи на "+id[1]+" с "+id[2]+" до "+id[3]+"</h4>")
        });
        $("#form-modal").modal('show');
        ev.stopPropagation();
    });
});