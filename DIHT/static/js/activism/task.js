$(function() {
    var fields = {'#desc': 'description', '#est-hours': 'hours_predict', '#num':'number_of_assignees', '#limit': 'datetime_limit'};

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
            a.push($(this).text());
        });
        return a;
    }

    function post_ajax(dict){
        var dat = {};
        $.each(fields, function (key, value) {
            dat[value] = $(key+'-current').text();
        });

        dat['event'] = $('#event-current').text();
        dat['assignees'] = get_ids('.assignee');
        dat['candidates'] = get_ids('.candidate');
        dat['rejected'] = get_ids('.rejected');

        for (key in dict)
            dat[key] = dict[key];
        dat['datetime_limit'] = dat['datetime_limit'].replace('T', ' ');

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
            post_ajax(dict);
            transfer_class('hidden', key, key+'-edit');
        });
	});

    // Events
    $('#event-pencil').click(function() {
	    transfer_class('hidden', '#event-edit', '#event');
		$('#event-edit').focus();
	})

	$('#event-edit').blur(function() {
	    post_ajax({'event': $('#event-edit option:selected').val()})
		transfer_class('hidden', '#event', '#event-edit');
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


    // Resign
	$('.resign').click(function() {
		resign_id = $(this).prev()[0].id;
		var assignees = get_ids('.assignee');
        assignees.splice($.inArray(resign_id, assignees), 1);
        post_ajax({'assignees': assignees});
	})


	// Approve
	$('.approve').click(function() {
		approve_id = $(this).prev()[0].id;
		var candidates = get_ids('.candidate');
		candidates.splice($.inArray(approve_id, candidates), 1);
		var assignees = get_ids('.assignee');
		assignees.push(approve_id);
        post_ajax({'candidates': candidates, 'assignees': assignees});
	})


    // Reject
	$('.reject').click(function() {
		reject_id = $(this).prev().prev()[0].id;
		var candidates = get_ids('.candidate');
		candidates.splice($.inArray(reject_id, candidates), 1);
		var rejected = get_ids('.rejected');
		rejected.push(reject_id);
        post_ajax({'candidates': candidates, 'rejected': rejected});
	})

	// Confirm modals
	$('.confirm').click(function(ev){
	    ev.preventDefault();
	    $('#confirm-modal').modal('show');
	    var btn_href = $(this)[0].href
        $('#submit-modal').click(function(ev){
            $('#confirm-modal').modal('hide');
            window.location.replace(btn_href);
        })
	})

});