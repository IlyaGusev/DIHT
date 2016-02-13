$(function(){
    $('.month-selector').on('change',function(event){
        event.preventDefault();
        $(".div-rating").addClass("hidden");
        var option =  $(".month-selector option:selected").val()
        $("#"+option).removeClass("hidden");
    })

    $(document).ready(function() {
        var option =  $(".month-selector option:selected").val()
	    $("#"+option).removeClass("hidden");
    });

    $('.expand').on('click', function(event){
       arrow = $($(this).children("i")[0])
       table = $($(this).siblings()[0])
        if (arrow.hasClass("fa-caret-down")) {
            arrow.removeClass("fa-caret-down")
            arrow.addClass("fa-caret-up")
            table.removeClass("hidden")
        } else {
            arrow.removeClass("fa-caret-up")
            arrow.addClass("fa-caret-down")
            table.addClass("hidden")
        }
    });
    
});
