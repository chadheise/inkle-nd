$(document).ready(function() {
    function hideMemberCard(memberID) {
        $("#memberCard_" + memberID).fadeOut('medium');
    }
    
    /*----------------------Circle Button Functions--------------------------*/
    $(".circlesCardButton").live("mouseenter", function() {
        var memberID = $(this).attr("memberID");
        if ($("#circlesMenu_"+memberID).attr("showing") == "false") {
            $(".circlesMenu").fadeOut('medium');
            var buttonPosition = $(this).position();
            var buttonHeight = $(this).height();
            $("#circlesMenu_"+memberID).css('left', buttonPosition.left);
            $("#circlesMenu_"+memberID).css('top', buttonPosition.top + 2*buttonHeight);
            $("#circlesMenu_"+memberID).fadeIn('medium');
            $(".circleMenu").attr("showing", "false");
            $("#circlesMenu_"+memberID).attr("showing", "true");
        }
    });
    
    $(".circlesCardButton").live("click", function() {
        var memberID = $(this).attr("memberID");
        $("#circlesMenu_"+memberID).fadeToggle('medium');
         if ($("#circlesMenu_"+memberID).attr("showing") == "true") {
             $(".circleMenu").attr("showing", "false");
             //$("#circlesMenu_"+memberID).attr("showing", "false");
         }
         else {
             $(".circleMenu").attr("showing", "false");
             $("#circlesMenu_"+memberID).attr("showing", "true");
         }
    });
    
    $(".circlesMenu").live("mouseleave", function() {
        $(this).fadeOut('medium');
        $(this).attr("showing", "false");
    });
    
    $(".circlesMenuItem").live("change", function() {
        var circleID = parseInt($(this).attr("circleID"));
        var toMemberID = parseInt($(this).attr("toMemberID"));
        var currentCircle = parseInt($(".selectedCircle").attr("circleID"));
        
        if ($(this).is(':checked')) { var URL = "/inkle/addToCircle/" } //If it is checked
        else { var URL = "/inkle/removeFromCircle/" } //If it is un-checked
        
        $.ajax({
            type: "POST",
            url: URL,
            data: { "circleID" : circleID,
                    "toMemberID" : toMemberID},
            success: function(html) {},
            error: function(a, b, error) { alert(error); }
        });
        
        if (circleID == currentCircle || currentCircle == -1) {
           hideMemberCard(toMemberID);
        }
    });
    
    /*----------------------Prevent Following Button --------------------------*/
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
    
    /*----------------------Stop Following Button --------------------------*/
    $(".stopFollowing").live("click", function() {
            var thisElement = $(this);
            var toMemberID = parseInt($(this).attr("memberID"));
            
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
            
            if ($(".selectedCircle").attr("circleID")) {
               hideMemberCard(toMemberID);
            }
            else {
                $(".circlesCardButton").each(function() {
                    if ($(this).attr("memberID") == toMemberID) {
                        $(this).fadeOut('medium');
                    }
                });
            }
        });
        
    /*----------------------Request to Following Button --------------------------*/
    $(".requestToFollow").live("click", function() {
        var thisElement = $(this);
        var toMemberID = parseInt($(this).attr("memberID"));
        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/inkle/requestToFollow/",
            data: { "toMemberID" : toMemberID },
            success: function(title) {
                thisElement.val("Revoke request");
                thisElement.addClass("revokeRequest");
                thisElement.removeClass("requestToFollow");
                thisElement.attr("title", title);
            },
            error: function(a, b, error) { alert(error); }
        });
    });
    
    // Revoke request button
    $(".revokeRequest").live("click", function() {
        var thisElement = $(this);
        var toMemberID = parseInt($(this).attr("memberID"));
        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/inkle/revokeRequest/",
            data: { "toMemberID" : toMemberID },
            success: function(title) {
                if (thisElement.parents("#requestsContent").length != 0)
                {
                    // Alert the user that they revoked the request
                    var memberCard = thisElement.parents(".memberCard");
                    var memberCardName = memberCard.find(".memberCardName").text();
                    memberCard.fadeOut(function() {
                        memberCard.html("You revoked your request to follow " + memberCardName + ".");
                        memberCard.css("padding", "10px");
                        memberCard.fadeIn("medium").delay(2000).fadeOut("medium", function() {
                            if ($("#pendingRequestsContent").has(".memberCard:visible").length == 0)
                            {
                                $("#pendingRequestsContent").fadeOut("medium", function() {
                                    $("#pendingRequestsContent").html("<p class='requestsTitle'>You have no pending requests to follow anyone.</p>");
                                    $("#pendingRequestsContent").fadeIn("medium");
                                });
                            }
                        });
                    });
                }
                else
                {
                    thisElement.val("Request to follow");
                    thisElement.removeClass("revokeRequest");
                    thisElement.addClass("requestToFollow");
                    thisElement.attr("title", title);
                }
            },
            error: function(a, b, error) { alert(error); }
        });
    });
    
});
