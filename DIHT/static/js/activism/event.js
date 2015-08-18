$(function() {
    function transfer_class(attr, elem2, elem1){
        $(elem1).addClass(attr);
		$(elem2).removeClass(attr);
    };

    function dict_to_string(dat){
        st = '';
        for (var key in dat)
            if (!Array.isArray(dat[key]))
                st+='&'+key+'='+dat[key];
            else
                for (var elem in dat[key])
                    st+='&'+key+'='+dat[key][elem];
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

    function post_ajax(dict){
        var dat = {};
        dat['description'] = $('#desc').text();
        dat['date_held'] = $('#date_held_formatted').text();
        dat['assignees'] = get_ids('.assignee');

        for (key in dict)
            dat[key] = dict[key];
        data = dict_to_string(dat);
        $.ajax({
            type: 'POST',
            url: window.location.href,
            data: data,
            success: function(data) {
                window.location.reload();
            },
            error: function(request, status, error) {
                console.log(error)
            }
        });
    };

	// Description
	$('#desc-pencil').click(function() {
	    transfer_class('hidden', '#desc-area', '#desc');
		$('#desc-area').focus();
	})

	$('#desc-area').blur(function() {
	    post_ajax({'description': $('#desc-area').val()})
		transfer_class('hidden', '#desc', '#desc-area');
	})


	// Assign
	$('#assign').click(function() {
		transfer_class('hidden', '#id_assignees_autocomplete-autocomplete', '#assign');
		$('#id_assignees_autocomplete-autocomplete').focus();
	})

	$('#id_assignees_autocomplete-autocomplete').blur(function() {
	    var assignees = get_ids('.assignee');
        assignees.push($("#id_assignees_autocomplete option:selected" ).val())
        post_ajax({'assignees': assignees});
        transfer_class('hidden', '#assign', '#id_assignees_autocomplete-autocomplete');
	})


	// Date_held
	$('#date_held-pencil').click(function() {
		transfer_class('hidden', '#dateedit', '#date_held');
		$('#datepicker').focus();
	})

	$('#datepicker').blur(function() {
        post_ajax({'date_held': ($("#datepicker").val()).split(' ')[0]})
        transfer_class('hidden', '#date_held', '#dateedit');
	})


    // Resign
	$('.resign').click(function() {
		resign_id = $(this).prev()[0].id;
		var assignees = get_ids('.assignee');
        assignees.splice($.inArray(resign_id, assignees), 1);
        post_ajax({'assignees': assignees});
	})
});