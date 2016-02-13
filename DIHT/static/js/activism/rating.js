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
});