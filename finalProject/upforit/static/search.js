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
        
        if ($(this).val() == "All")
        {
            $(".filterButton").addClass("selected");
            
            $("#searchContent").fadeOut(function() {
                $("#people").show();
                $("#locations").show();
                $("#spheres").show();

                $("#searchContent").fadeIn();
            });
        }
        else
        {
            $(".filterButton").removeClass("selected");
            $(this).addClass("selected");

            if ($(this).val() == "People")
            {
                $("#searchContent").fadeOut(function() {
                    $("#people").show();
                    $("#locations").hide();
                    $("#spheres").hide();

                    $("#searchContent").fadeIn();
                });
            }
            else if ($(this).val() == "Locations")
            {
                $("#searchContent").fadeOut(function() {
                    $("#people").hide();
                    $("#locations").show();
                    $("#spheres").hide();

                    $("#searchContent").fadeIn();
                });
            }
            else if ($(this).val() == "Spheres")
            {
                $("#searchContent").fadeOut(function() {
                    $("#people").hide();
                    $("#locations").hide();
                    $("#spheres").show();

                    $("#searchContent").fadeIn();
                });
            }
        }
        
    });
   
});
