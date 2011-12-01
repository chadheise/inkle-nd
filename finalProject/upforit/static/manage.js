$(document).ready(function() {
    $(".navButton").click(function() {
        var thisElement = $(this);
        //var member = $("#primaryContent").attr("member");

        if ($(this).val() == "Requests")
        {
            // Get Requests HTML
            $.ajax({
                type: "POST",
                url: "/upforit/requested/",
                data: {},
                success: function(html) {
                    $("#primaryContent").html(html);
                },
                error: function(a, b, error) { alert(error); }
            });
        }
            
    });

    
});
