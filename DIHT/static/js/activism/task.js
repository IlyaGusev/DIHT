$(function() {
    var fields = ['description', 'hours_predict', 'number_of_assignees', 'datetime_limit', 'event', 'sector', 'name'];
    var select_fields = ['event', 'sector'];
    var ajax_fields = ['description',  'hours_predict', 'number_of_assignees', 'name'];

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

    function post_task(dict){
        var reload = false
        for (key in dict)
            if (($.inArray(key, ajax_fields)) == -1)
                reload = true
        if ('datetime_limit' in dict)
            dict['datetime_limit'] = dict['datetime_limit'].replace('T', ' ');
        dict = dict_remove_empty(dict);
        $.ajax({
            type: 'POST',
            url: window.location.href,
            data: dict,
            success: function(response) {
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
            post_task(dict);
        });
	});

    // Tags
	$('#tags-pencil').click(function() {
	    transfer_class('hidden', '#tags-edit', '#tags');
		$('#id_tags').focus();
	})

    $('#id_tags').blur(function() {
	    post_task({'tags': $('#id_tags').val()})
		transfer_class('hidden', '#tags', '#tags-edit');
	})


	// Assign
	$('#assign').click(function() {
		transfer_class('hidden', '#id_assignees_autocomplete-autocomplete', '#assign');
		$('#id_assignees_autocomplete-autocomplete').focus();
	})

	$('#id_assignees_autocomplete-autocomplete').blur(function() {
	    var assignees = get_ids('.assignee');
        assignees.push($("#id_assignees_autocomplete option:selected" ).val())
        post_task({'assignees_pk': assignees});
        transfer_class('hidden', '#assign', '#id_assignees_autocomplete-autocomplete');
	})


    // Resign
	$('.resign').click(function() {
		resign_id = $(this)[0].id;
		var assignees = get_ids('.assignee');
        assignees.splice($.inArray(resign_id, assignees), 1);
        post_task({'assignees_pk': assignees});
	})


	// Assign responsible
	$('#assign-responsible').click(function() {
		transfer_class('hidden', '#id_responsible_autocomplete-autocomplete', '#assign-responsible');
		$('#id_responsible_autocomplete-autocomplete').focus();
	})

	$('#id_responsible_autocomplete-autocomplete').blur(function() {
	    var responsible = get_ids('.responsible');
        responsible.push($("#id_responsible_autocomplete option:selected" ).val())
        post_task({'responsible': responsible});
        transfer_class('hidden', '#assign', '#id_responsible_autocomplete-autocomplete');
	})

    // Resign responsible
	$('.resign-responsible').click(function() {
		resign_id = $(this)[0].id;
		var responsible = get_ids('.responsible');
        responsible.splice($.inArray(resign_id, responsible), 1);
        post_task({'responsible': responsible});
	})


	// Approve
	$('.approve').click(function() {
		approve_id = $(this)[0].id;
		var candidates = get_ids('.candidate');
		candidates.splice($.inArray(approve_id, candidates), 1);
		var assignees = get_ids('.assignee');
		assignees.push(approve_id);
        post_task({'candidates': candidates, 'assignees_pk': assignees});
	})


    // Reject
	$('.reject').click(function() {
		reject_id = $(this)[0].id;
		var candidates = get_ids('.candidate');
		candidates.splice($.inArray(reject_id, candidates), 1);
		var rejected = get_ids('.rejected');
		rejected.push(reject_id);
        post_task({'candidates': candidates, 'rejected': rejected});
	})

	$(document).ready(function() {
	    if ($('.event-current').length)
            if ($('.event-current')[0].id!='')
                $('#event-field option[value='+$('.event-current')[0].id+']').attr("selected",true);
        if ($('.sector-current').length)
            if ($('.sector-current')[0].id!='')
                $('#sector-field option[value='+$('.sector-current')[0].id+']').attr("selected",true);
    });

    $('#prop-modal').on('shown.bs.modal', function () {
        if ($('#hard').length)
            $(this).find('#id_is_hard').prop('checked', true);
        else
            $(this).find('#id_is_hard').prop('checked', false);
        if ($('#urgent').length)
            $(this).find('#id_is_urgent').prop('checked', true);
        else
            $(this).find('#id_is_urgent').prop('checked', false);
    });

    $("#comment-create").on('click', function(event){
        event.preventDefault();
        var href = $(this)[0].href;
        var text = $("#comment-field-new").val();
        if (text != "")
            $.ajax({
                type: 'POST',
                url: href,
                data: {'text': text},
                success: function(response) {
                    window.location.reload();
                },
                error: function(request, status, error) {
                    console.log(error)
                }
            });
    });
    
    $("#comment-field-new").on('submit', function(event){
        event.preventDefault();
        var href = $(this)[0].href;
        var text = $("#comment-field-new").val();
        if (text != "")
            $.ajax({
                type: 'POST',
                url: href,
                data: {'text': text},
                success: function(response) {
                    window.location.reload();
                },
                error: function(request, status, error) {
                    console.log(error)
                }
            });
    });

    
    $('.comment-pencil').click(function(event) {
        event.preventDefault();
        var comment_current = $(this).parents('.comment-current')
        var comment_edit = comment_current.siblings('.comment-edit')
        transfer_class('hidden', comment_edit, comment_current);
        comment_edit.find('.comment-field').focus();
    });

    $('.comment-field').blur(function() {
        var text = $(this).val();
        var id = $(this)[0].id;
        var comment_edit = $(this).parents('.comment-edit');
        var comment_current = comment_edit.siblings('.comment-current');
        var href = comment_current.find(".comment-pencil")[0].href
        console.log(href)
        $.ajax({
            type: 'POST',
            url: href,
            data: {'text': text},
            success: function(response) {
                window.location.reload();
            },
            error: function(request, status, error) {
                console.log(error)
            }
        });
        transfer_class('hidden', comment_current, comment_edit);
    });
});