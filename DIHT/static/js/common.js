$(function() {
    $("a[data-target=#form-modal],th[data-target=#form-modal]").click(function(ev) {
        ev.preventDefault();
        var target = $(this).attr("href");
        $("#form-modal .modal-content").load(target, function() {
             $("#form-modal").modal("show");
        });
        return false;
    });
});