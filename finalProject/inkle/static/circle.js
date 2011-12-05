$(document).ready(function() {
    // Change circle color and members when clicked
    $(".circle").live("click", function() {
        $(".selectedCircle").removeClass("selectedCircle");
        $(this).addClass("selectedCircle");
        
        if ($(this).attr("id") != "newCircle")
        {
            var circleID = parseInt($(this).attr("circleID"));

            $.ajax({
                type: "POST",
                url: "/inkle/circleMembers/",
                data: { "circleID" : circleID },
                success: function(html) {
                    $("#circleMembers").html(html);
                },
                error: function(a, b, error) { alert(error); }
            });
        }
    });

    $("#addCircleButton").live("click", function() {
        $(this).before("<button id='newCircle' class='circle'><input id='newCircleInput' type='text' /></button>");
        $(".selectedCircle").removeClass("selectedCircle");
        $("#newCircle").addClass("selectedCircle");
        $("#newCircleInput").focus();
        $(this).hide();
    });

    $("#newCircleInput").live("blur", function() {
        var newCircleName = $("#newCircleInput").val();
        if (newCircleName == "")
        {
            $("#newCircle").remove();
            $(".circle:last").trigger("click");
        }
        else
        {
            $.ajax({
                type: "POST",
                url: "/inkle/addCircle/",
                data: { "circleName" : newCircleName },
                success: function(circleID) {
                    $("#newCircle").attr("circleID", circleID);
                    $("#newCircle").removeAttr("id");
                },
                error: function(a, b, error) { alert(error); }
            });
            
            $("#newCircle").html(newCircleName);

        }
        $("#addCircleButton").show();
    });
    
    // Remove member from circle
    $(".remove").live("click", function() {
        var toMemberID = parseInt($(this).attr("memberID"));
        var circleID = parseInt($(".selectedCircle").attr("circleID"));
        
        $.ajax({
            type: "POST",
            url: "/inkle/removeFromCircle/",
            data: { "toMemberID" : toMemberID, "circleID" : circleID },
            success: function(html) {
            },
            error: function(a, b, error) { alert(error); }
        });

        $(this).hide();
    });

    // Add member to circle
    $(".add").live("click", function() {
        $(this).next("hi");
    });

});
