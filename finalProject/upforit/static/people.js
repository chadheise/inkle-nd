$(document).ready(function() {
    $(".friendRequestButton").click(function() {
        if ($(this).val() == "Request friend")
        {
            var toMemberID = parseInt($(this).attr("memberID"));

            // Send friend request to database
            $.ajax({
                type: "POST",
                url: "/upforit/friendRequest/",
                data: { "toMemberID" : toMemberID }
            });
        
            $(this).val("Revoke request");
            $(this).addClass("requestPending");
        }
        else if ($(this).val() == "Revoke request")
        {
            var toMemberID = parseInt($(this).attr("memberID"));

            // Send friend request to database
            $.ajax({
                type: "POST",
                url: "/upforit/revokeRequest/",
                data: { "toMemberID" : toMemberID }
            });
        
            $(this).val("Request friend");
            $(this).removeClass("requestPending");
        }
    });
});
