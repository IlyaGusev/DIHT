$(function() {
    var fields = ['description', 'date_held', 'sector'];
    var select_fields = ['sector'];
    var ajax_fields = ['description'];
    function transfer_class(attr, elem2, elem1){
        $(elem1).addClass(attr);
		$(elem2).removeClass(attr);
    };

    function dict_remove_empty(dat){
        for (var key in dat)
            if (Array.isArray(dat[key]))
                if (dat[key].length == 0)
                    dat[key] = 'None'
        return dat;
    };


    function get_ids(selector){
        var a = [];
        $(selector).each(function() {
            a.push($(this)[0].id);
        });
        return a;
    }

    function post_event(dict){
        var reload = false
        for (key in dict)
            if (($.inArray(key, ajax_fields)) == -1)
                reload = true
        dict = dict_remove_empty(dict);
        $.ajax({
            type: 'POST',
            url: window.location.href,
            data: dict,
            success: function(data) {
                if (reload)
                    window.location.reload();
                else{
                    for (field in dict){
                        if (($.inArray(field, ajax_fields)) != -1){
                            if (($.inArray(field, select_fields)) == -1){
                                var elem = $('#'+field+'-current')
                                elem.text($('#'+field+'-field').val())
                                elem.html(elem.html().replace(/\r\n|\r|\n/g,'<br>'))
                            }
                        }
                    }
                }
            },
            error: function(request, status, error) {
                console.log(error)
            }
        });
    };

	$.each(fields, function (index, key) {
        var field = '#'+key
	    $(field+'-pencil').click(function() {
            transfer_class('hidden', field+'-edit', field);
            $(field+'-field').focus();
        });

        $(field+'-field').blur(function() {
            transfer_class('hidden', field, field+'-edit');
            var dict = {}
            if (($.inArray(field, select_fields)) == -1)
                dict[key] = $(field+'-field').val()
            else
                dict[key] = $(field+'-field option:selected').val()
            post_event(dict);
        });
	});


	// Assign responsible
	$('#assign').click(function() {
		transfer_class('hidden', '#id_responsible_autocomplete-autocomplete', '#assign');
		$('#id_responsible_autocomplete-autocomplete').focus();
	})

	$('#id_responsible_autocomplete-autocomplete').blur(function() {
	    var responsible = get_ids('.responsible');
        responsible.push($("#id_responsible_autocomplete option:selected" ).val())
        post_event({'responsible': responsible});
        transfer_class('hidden', '#assign', '#id_responsible_autocomplete-autocomplete');
	})


    // Resign
	$('.resign').click(function() {
		resign_id = $(this)[0].id;
		var responsible = get_ids('.responsible');
        responsible.splice($.inArray(resign_id, responsible), 1);
        post_event({'responsible': responsible});
	})

    $(document).ready(function() {
        if ($('.sector-current').length)
            if ($('.sector-current')[0].id!='')
                $('#sector-field option[value='+$('.sector-current')[0].id+']').attr("selected",true);
    });
});