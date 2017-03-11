$(function() {
    $('#form-modal').on('submit', '#create-record-form,#cancel-record-form', function (ev) {
        ev.preventDefault();
        var form = $(this);
        id = $(current_edit_span)[0].id.split(" ");
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
        var val = $("#machine_id option:selected" ).val();
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
        id = $(current_edit_span)[0].id.split(" ");
        $("#form-modal").find(".modal-content").load($(this).attr("href"), function() {
            machine_name = $("#machine_"+id[0]).text()
            $(this).find("#create-record-body").html("<h4>Оплатить "+machine_name+" на "+id[1]+" с "+id[2]+" до "+id[3]+"</h4>")
            $(this).find("#create-record-submit").html("Оплатить ("+id[4]+' <img style="margin-top:-3px;" src="/static/img/icons/fivt_coin_tiny_w.png">)')
            $(this).find("#cancel-record-body").html("<h4>Отказаться от записи на "+id[1]+" с "+id[2]+" до "+id[3]+"</h4>")
        });
        $("#form-modal").modal('show');
        return false;
    });
});

$(document).ready(function(){
     $('.spoiler_links').click(function(){
      $(this).parent().parent().children('div.washing_instruction').toggle('normal');
      return false;
     });
    /*$("#activist_btn").click(function(){
    //document.getElementById("usual_washing").style.display="none";
    //document.getElementById("activist_washing").style.display="";
        $.ajax({
            type: "POST",
            url: "/washing/",
            data: {check_op: "true"}
        }).done(function (msg) {
            if(msg == "false") {
                msg = "Недостаточно очков роста";
                alert(msg);
            }
        });
    return false;
        });*/
    $.ajax({
            type: "POST",
            url: "/washing/",
            data: {check_op: "continue"}
        }).done(function (msg) {
        if(msg != "false")
            document.getElementById("activist_tabs").style.display="inline-block";
        });
    $('input[name="cancel_activ"]').click(function () {
        //var user_id = this.id.substr(13, 14);
        var id = this.id.split(" ");
        var user_id = id[0].substr(13, 10);
        $.ajax({
            type: "POST",
            url: "/washing/",
            data: {
                'cancel_id': user_id,
                'machine' : id[1],
                'date' : id[2],
                'time_from': id[3],
                'time_to': id[4],
            }
        }).done(function (msg) {
            window.location.reload();
        });
    });
    });