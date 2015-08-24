$(function() {
    function view_modal_errors(form, request){
        errors = JSON.parse(request.responseText);
        $('.errorlist').remove();
        for (var k in errors)
            form.find('#id_'+k).after('<ul class="errorlist"><li>' + errors[k] + '</li></ul>');
    }

    $('#form-modal').on('shown.bs.modal', function () {
        if ($(this).find('form').hasClass('task-create-form'))
            if ($('.event-name').text() != ""){
                $(this).find("#id_event option:contains("+$('.event-name').text()+")").attr('selected','selected');
                $(this).find("#id_sector option:contains("+$('.sector-name').text()+")").attr('selected','selected');
            }
    });

    $('#form-modal').on('submit', '.task-create-form,.event-create-form', function(ev) {
        ev.preventDefault();
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


     // Task actions
    function post_action(url, data){
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            success: function(response) {
                window.location.replace(response.url)
            },
            error: function(request, status, error) {
                console.log(error)
            }
        });
    }

	$('.action').click(function(ev){
	    ev.preventDefault();
	    var btn = $(this)
	    var btn_href = $(this)[0].href
	    if (btn.hasClass('confirm')){
	        $('#confirm-modal').modal('show');
            $('#submit-modal').click(function(ev){
                $('#confirm-modal').modal('hide');
                post_action(btn_href)
            })
	    }
	    else{
	        if (btn[0].id=='resolved'){
	            $('#resolve-modal').on('submit', '.resolve-form', function(ev) {
	                ev.preventDefault();
                    post_action(btn_href, $(this).serialize());
                    return false;
                })
	            $('#resolve-modal').modal('show');
	        }
	        else if (btn[0].id=='close'){
	            $('#close-modal').on('submit', '.close-form', function(ev) {
	                ev.preventDefault();
                    post_action(btn_href, $(this).serialize());
                    return false;
                })
	            $('#close-modal').modal('show');
	        }
	        else
	            post_action(btn_href)
	    }
	})

	$('#close-modal').on('shown.bs.modal', function () {
        $(this).find('.real-hours').each(function() {
            var inp = $(this)
            inp.next().find('.final-hours').text(inp.val())
            inp.next().next().val(inp.val())
            $('#close-modal').on('change', '.real-hours', function(ev){
                inp.next().find('.final-hours').text(inp.val())
                inp.next().next().val(inp.val())
            })
        });
    });
});