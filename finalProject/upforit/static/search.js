$(document).ready(function() {
    $(".cardButton").click(function() {
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
                    thisElement.addClass("revokeRequest");
                    thisElement.removeClass("requestToFollow");
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
                    thisElement.addClass("requestToFollow");
                    thisElement.removeClass("revokeRequest");
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
                        thisElement.addClass("requestToFollow");
                        thisElement.removeClass("stopFollowing");
                    },
                    error: function(a, b, error) { alert(error); }
                });
            
        }
    });
    
    $(".filterButton").click(function() {
        var thisElement = $(this);
        
        if (thisElement.val() == "All")
        {
             $(".filterButton").addClass("selected");          
        }
        else
        {
             $(".filterButton").removeClass("selected"); 
             thisElement.addClass("selected");         
        }
        
    });
    
});
