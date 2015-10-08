$(function() {
    $(document).ready(function() {
        $('.assignee-input').each(function() {
            input = $(this)
            var selector = $('#cur_'+$(this)[0].id)
            if (!selector.hasClass('red') && !selector.hasClass('blue')){
                if (selector.text() != '')
                    input.val(selector.text())
            }
        });
    });
});