$(document).ready(function() {
    $(".acceptRequestButton").click(function() {
        var fromMemberID = parseInt($(this).attr("memberID"));

        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/upforit/acceptRequest/",
            data: { "fromMemberID" : fromMemberID },
            error: function (a, b, c) { alert(c); }
        });
        
        //$(this).val("Revoke request");
        //$(this).addClass("requestPending");
    });
    
    $(".rejectRequestButton").click(function() {
        var fromMemberID = parseInt($(this).attr("memberID"));

        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/upforit/rejectRequest/",
            data: { "fromMemberID" : fromMemberID },
            error: function (a, b, c) { alert(c); }
        });
        
        //$(this).val("Revoke request");
        //$(this).addClass("requestPending");
    });
});
