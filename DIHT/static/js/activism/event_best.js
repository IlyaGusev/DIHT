$(function() {
    $(".event-best-on").on("click", function(event){
        event.preventDefault();
        var href = $(this)[0].href;
        var text = "Лучший активист " + $(".event-name").text();
        $.ajax({
            type: 'POST',
            url: href,
            data: {'amount': 1, 'description': text},
            success: function(response) {
                window.location.reload();
            },
            error: function(request, status, error) {
                console.log(error)
            }
        });
    })
});