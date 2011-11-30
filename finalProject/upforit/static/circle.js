$(document).ready(function() {
    // Toggle location edit content
    $(".circle").click(function() {
        $("#selectedCircle").attr("id", "");
        $(this).attr("id", "selectedCircle");
    
        var circleID = parseInt($(this).attr("circleID"));

        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/upforit/circleMembers/",
            data: { "circleID" : circleID },
            success: function(html) {
                $("#circleMembers").html(html);
            },
            error: function(a, b, error) { alert(error); }
        });
        
    });
});
