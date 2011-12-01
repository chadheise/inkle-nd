$(document).pageLoad(function() {

    // Change circle color and members when clicked
    $(".circle").click(function() {
        $("#selectedCircle").attr("id", "");
        $(this).attr("id", "selectedCircle");
    
        var circleID = parseInt($(this).attr("circleID"));

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
    
    // Remove member from circle
    $(".removeMemberButton").live("click", function() {
        var toMemberID = parseInt($(this).attr("memberID"));
        var circleID = parseInt($("#selectedCircle").attr("circleID"));
        
        $.ajax({
            type: "POST",
            url: "/upforit/removeFromCircle/",
            data: { "toMemberID" : toMemberID, "circleID" : circleID },
            success: function(html) {
            },
            error: function(a, b, error) { alert(error); }
        });

        $(this).hide();
    });
});
