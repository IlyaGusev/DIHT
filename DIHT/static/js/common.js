$(function() {
    // Modal popup
    $("body").on("click", ".btn-open-modal", function(ev) {
        ev.preventDefault();
        current_edit_span = $(this)[0];
        $("#form-modal").find(".modal-content").load($(this).attr("href"));
        $("#form-modal").modal('show');
        return false;
    });
});

