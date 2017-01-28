$(function() {
    $("#payments_apply").click(function(ev) {
        ev.preventDefault();
        $("#submit-modal").click(function(ev) {
            post_action("./", {
                    const: $('#const').val(),
                    begin: $('#begin').val(),
                    end: $('#end').val(),
                });
        });
    });
});