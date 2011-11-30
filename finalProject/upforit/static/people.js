$(document).ready(function() {
    $(".followRequestButton").click(function() {
        var thisElement = $(this);
        var toMemberID = parseInt($(this).attr("memberID"));
        
        if ($(this).val() == "Request to follow")
        {
            // Send friend request to database
            $.ajax({
                type: "POST",
                url: "/upforit/followRequest/",
                data: { "toMemberID" : toMemberID },
                success: function(html) {
                    thisElement.val("Revoke request");
                    thisElement.addClass("requestPending");
                },
                error: function(a, b, error) { alert(error); }
            });
        }
        else if ($(this).val() == "Revoke request")
        {
            // Send friend request to database
            $.ajax({
                type: "POST",
                url: "/upforit/revokeRequest/",
                data: { "toMemberID" : toMemberID },
                success: function(html) {
                    thisElement.val("Request to follow");
                    thisElement.removeClass("requestPending");
                },
                error: function(a, b, error) { alert(error); }
            });
        }
        else if ($(this).val() == "Stop following")
            {
                // Send friend request to database
                $.ajax({
                    type: "POST",
                    url: "/upforit/stopFollowing/",
                    data: { "toMemberID" : toMemberID },
                    success: function(html) {
                        thisElement.val("Request to follow");
                        thisElement.removeClass("stopFollowing");
                    },
                    error: function(a, b, error) { alert(error); }
                });
            
        }
    });
});
