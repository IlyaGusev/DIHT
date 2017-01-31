$(function() {
    function get_payments_table_data() {
        return {
            const: $('#const').val(),
            begin: $('#begin').val(),
            end: $('#end').val(),
        }
    }

    $("#payments_apply").click(function(ev) {
        ev.preventDefault();
        $("#submit-modal").click(function(ev) {
            post_action("./", get_payments_table_data());
        });
    });

    $("#download_csv").click(function(ev) {
        ev.preventDefault();
        window.location.replace(window.location.pathname + "as_csv/" + window.location.search)
    });
});