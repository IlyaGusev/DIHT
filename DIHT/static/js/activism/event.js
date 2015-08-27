$(function() {
    var fields = {'#desc': 'description', '#date_held': 'date_held'};
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

    function post_event(dict){
        var dat = {};
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

	$.each(fields, function (key, value) {
	    $(key+'-pencil').click(function() {
            transfer_class('hidden', key+'-edit', key);
            $(key+'-field').focus();
        });

        $(key+'-field').blur(function() {
            var dict = {}
            dict[value] = $(key+'-field').val()
            post_event(dict);
            transfer_class('hidden', key, key+'-edit');
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
		resign_id = $(this).prev()[0].id;
		var assignees = get_ids('.assignee');
        assignees.splice($.inArray(resign_id, assignees), 1);
        post_event({'assignees': assignees});
	})

	// Sectors
    $('#sector-pencil').click(function() {
	    transfer_class('hidden', '#sector-edit', '#sector');
		$('#sector-edit').focus();
	})

	$('#sector-edit').blur(function() {
	    post_event({'sector': $('#sector-edit option:selected').val()})
		transfer_class('hidden', '#sector', '#sector-edit');
	})

    $(document).ready(function() {
        if ($('.sector-current')[0].id!='')
            $('#sector-edit option[value='+$('.sector-current')[0].id+']').attr("selected",true);
    });
});