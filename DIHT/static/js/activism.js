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

$(function() {
    $('#form-modal').on('shown.bs.modal', function () {
        if ($(this).find('form').hasClass('task-create-form'))
            if ($('.event-name').text() != ""){
                $(this).find("#id_event option:contains("+$('.event-name').text()+")").attr('selected','selected');
                $(this).find("#id_sector option:contains("+$('.sector-name').text()+")").attr('selected','selected');
            }
    });

    $('#confirm-modal').on('hide.bs.modal', function() {
        $('#submit-modal').off('click');
    });

	$('.action').click(function(ev){
	    ev.preventDefault();
	    var btn = $(this)
	    var btn_href = $(this)[0].href
	    if (btn.hasClass('confirm')){
	        $('#confirm-modal').modal('show');
            $('#submit-modal').click(function(ev){
                $('#confirm-modal').modal('hide');
                if (btn_href) {
                    post_action(btn_href);
                }
            })
	    }
	    else{
	        var id = btn[0].id
	        if (id=='resolve' || id=='prop' || id=='close'){
	            $('#'+id+'-modal').on('submit', '.'+id+'-form', function(ev) {
	                ev.preventDefault();
                    post_action(btn_href, $(this).serialize());
                    return false;
                })
	            $('#'+id+'-modal').modal('show');
	        }
	        else
	            post_action(btn_href)
	    }
	})

	$('#close-modal').on('shown.bs.modal', function () {
        $(this).find('.real-hours').each(function() {
            var inp = $(this)
            var coef = 1
            if ($('#urgent').length || $('#hard').length)
                coef = 1.5
            if ($('#urgent').length && $('#hard').length)
                coef = 2
            var final = Number((inp.val()*coef).toFixed(2))
            inp.next().find('.final-hours').text(final);
            inp.next().next().val(final)
            $('#close-modal').on('change', '.real-hours', function(ev){
                final = Number((inp.val()*coef).toFixed(2))
                inp.next().find('.final-hours').text(final)
                inp.next().next().val(final)
            })
        });
    });

    $('#id_assignees_autocomplete-autocomplete, #id_responsible_autocomplete-autocomplete').on('input', function(){
        var st = $(this).val();
        if ((('a'<= st[0] && st[0] <= 'z') || ('а'<= st[0] && st[0] <= 'я')) && st.length > 0){
            $(this).val(st[0].toUpperCase() + st.slice(1));
        }
    });
});