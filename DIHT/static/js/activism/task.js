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
        dat['hours_predict'] = $('#est-hours').text().split(' ')[1];
        dat['description'] = $('#desc').text();
        dat['datetime_limit'] = $('#datelimit_formatted').text();
        dat['assignees'] = get_ids('.assignee');
        dat['candidates'] = get_ids('.candidate');
        dat['number_of_assignees'] = $('#num-field').val();
        dat['event'] = $('.event-name')[0].id;

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

    // Events
	$('#event-pencil').click(function() {
	    transfer_class('hidden', '#event-selector', '#event-noedit');
		$('#event-selector').focus();
		
	})
	
	$('#event-selector').blur(function() {
	    post_ajax({'event': $('#event-selector option:selected').val()})
		transfer_class('hidden', '#event-noedit', '#event-selector');
	})

	// Description
	$('#desc-pencil').click(function() {
	    transfer_class('hidden', '#desc-area', '#desc');
		$('#desc-area').focus();
	})

	$('#desc-area').blur(function() {
	    post_ajax({'description': $('#desc-area').val()})
		transfer_class('hidden', '#desc', '#desc-area');
	})

	// Hours
	$('#est-hours-pencil').click(function() {
		transfer_class('hidden', '#est-hours-edit', '#est-hours');
		$('#est-hours-field').focus();
	})
	
	$('#est-hours-field').blur(function() {
	    post_ajax({'hours_predict': $('#est-hours-field').val()})
		transfer_class('hidden', '#est-hours', '#est-hours-edit');
	})


	// Datetime_limit
	$('#datelimit-pencil').click(function() {
		transfer_class('hidden', '#dateedit', '#datelimit');
		$('#datepicker').focus();
	})
	
	$('#datepicker').blur(function() {
        post_ajax({'datetime_limit': ($("#datepicker").val()+' '+$("#timepicker").val()).split(' ')[0]})
        transfer_class('hidden', '#datelimit', '#dateedit');
	})


	// Number of assignees
	$('#num-pencil').click(function() {
		transfer_class('hidden', '#num-edit', '#num');
		$('#num-field').focus();
	})

	$('#num-field').blur(function() {
        post_ajax({'number_of_assignees': $('#num-field').val()});
        transfer_class('hidden', '#num', '#num-edit');
	})


	// Assign
	$('#assign').click(function() {
		transfer_class('hidden', '#assignee-selector', '#assign');
		$('#assignee-selector').focus();
	})

	$('#assignee-selector').blur(function() {
	    var assignees = get_ids('.assignee');
        assignees.push($("#assignee-selector option:selected" ).val())
        post_ajax({'assignees': assignees});
        transfer_class('hidden', '#assign', '#assignee-selector');
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

});