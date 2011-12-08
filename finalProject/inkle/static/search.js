$(document).ready(function() {
    $(".cardButton").click(function() {
        var thisElement = $(this);
        var toMemberID = parseInt($(this).attr("memberID"));
        
        if ($(this).val() == "Request to follow")
        {
            // Send friend request to database
            $.ajax({
                type: "POST",
                url: "/inkle/followRequest/",
                data: { "toMemberID" : toMemberID },
                success: function(title) {
                    thisElement.val("Revoke request");
                    thisElement.addClass("revokeRequest");
                    thisElement.removeClass("requestToFollow");
                    thisElement.attr("title", title);
                },
                error: function(a, b, error) { alert(error); }
            });
        }
        else if ($(this).val() == "Revoke request")
        {
            // Send friend request to database
            $.ajax({
                type: "POST",
                url: "/inkle/revokeRequest/",
                data: { "toMemberID" : toMemberID },
                success: function(title) {
                    thisElement.val("Request to follow");
                    thisElement.addClass("requestToFollow");
                    thisElement.removeClass("revokeRequest");
                    thisElement.attr("title", title);
                },
                error: function(a, b, error) { alert(error); }
            });
        }
        else if ($(this).val() == "Stop following")
            {
                // Send friend request to database
                $.ajax({
                    type: "POST",
                    url: "/inkle/stopFollowing/",
                    data: { "toMemberID" : toMemberID },
                    success: function() {
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
    
    $(".preventFollowing").live("click", function() {
        var thisElement = $(this);
        var fromMemberID = parseInt($(this).attr("memberID"));
        
        $.ajax({
            type: "POST",
            url: "/inkle/preventFollowing/",
            data: { "fromMemberID" : fromMemberID },
            success: function(html) {
                thisElement.remove();
            },
            error: function(a, b, error) { alert(error); }
        });
    });
   
    $(".joinSphere").live("click", function() {
        var thisElement = $(this);
        var sphereID = parseInt($(this).attr("sphereID"));
        
        $.ajax({
            type: "POST",
            url: "/inkle/joinSphere/",
            data: { "sphereID" : sphereID },
            success: function(html) {
                thisElement.val("Leave sphere");
                thisElement.addClass("leaveSphere");
                thisElement.removeClass("joinSphere");
            },
            error: function(a, b, error) { alert(error); }
        });
    });
    
    $(".leaveSphere").live("click", function() {
        var thisElement = $(this);
        var sphereID = parseInt($(this).attr("sphereID"));
        
        $.ajax({
            type: "POST",
            url: "/inkle/leaveSphere/",
            data: { "sphereID" : sphereID },
            success: function(html) {
                thisElement.val("Join sphere");
                thisElement.addClass("joinSphere");
                thisElement.removeClass("leaveSphere");
            },
            error: function(a, b, error) { alert(error); }
        });
    });
});
