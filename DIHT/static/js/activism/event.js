$(function() {
    var fields = ['description', 'date_held', 'sector'];
    var select_fields = ['sector'];
    var ajax_fields = ['description'];
    function transfer_class(attr, elem2, elem1){
        $(elem1).addClass(attr);
		$(elem2).removeClass(attr);
    };

    function dict_to_string(dat){
        st = '';
        for (var key in dat)
            if (!Array.isArray(dat[key]))
                st+='&'+key+'='+dat[key];
            else{
                if (dat[key].length == 0)
                    st+='&'+key+"=None";
                else
                    for (var elem in dat[key])
                        st+='&'+key+'='+dat[key][elem];
            }
        st = st.substr(1);
        return st;
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
        data = dict_to_string(dict);
        $.ajax({
            type: 'POST',
            url: window.location.href,
            data: data,
            success: function(data) {
                if (reload)
                    window.location.reload();
                else{
                    for (field in dict){
                        if (($.inArray(field, ajax_fields)) != -1){
                            if (($.inArray(field, select_fields)) == -1)
                                $('#'+field+'-current').text($('#'+field+'-field').val())
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


	// Assign
	$('#assign').click(function() {
		transfer_class('hidden', '#id_assignees_autocomplete-autocomplete', '#assign');
		$('#id_assignees_autocomplete-autocomplete').focus();
	})

	$('#id_assignees_autocomplete-autocomplete').blur(function() {
	    var assignees = get_ids('.assignee');
        assignees.push($("#id_assignees_autocomplete option:selected" ).val())
        post_event({'assignees': assignees});
        transfer_class('hidden', '#assign', '#id_assignees_autocomplete-autocomplete');
	})


    // Resign
	$('.resign').click(function() {
		resign_id = $(this)[0].id;
		var assignees = get_ids('.assignee');
        assignees.splice($.inArray(resign_id, assignees), 1);
        post_event({'assignees': assignees});
	})

    $(document).ready(function() {
        if ($('.sector-current')[0].id!='')
            $('#sector-field option[value='+$('.sector-current')[0].id+']').attr("selected",true);
    });
});