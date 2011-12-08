$(document).ready(function() {
    
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
    });
    
    /*----------------------Accept Request Button --------------------------*/
    $(".acceptRequest").live("click", function() {
        var fromMemberID = parseInt($(this).attr("memberID"));

        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/inkle/acceptRequest/",
            data: { "fromMemberID" : fromMemberID },
            error: function (a, b, c) { alert(c); }
        });
        
        var memberContainer = $(this).parent().parent();
        memberContainer.fadeOut(function(){
            memberContainer.html("Follow request accepted");
            memberContainer.fadeIn();
        });
    });
    
    /*----------------------Reject Request Button --------------------------*/
    $(".rejectRequest").live("click", function() {
        var fromMemberID = parseInt($(this).attr("memberID"));

        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/inkle/rejectRequest/",
            data: { "fromMemberID" : fromMemberID },
            error: function (a, b, c) { alert(c); }
        });
        
        var memberContainer = $(this).parent().parent();
        memberContainer.fadeOut(function(){
            memberContainer.html("Follow request rejected");
            memberContainer.fadeIn();
        });
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
    
    
    /*--*/
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
    /*--*/
    
});