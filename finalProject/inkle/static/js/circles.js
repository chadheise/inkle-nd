$(document).ready(function() {
    $("#addToCircleInput").live("focus", function() {
        if ($(this).val() == "Add people to this circle")
        {
            $(this).val("");
            $(this).css("color", "#000");
        }
    });
    
    $("#addToCircleInput").live("blur", function() {
        if ($(this).val() == "")
        {
            $(this).val("Add people to this circle");
            $(this).css("color", "#888");
        }
    });
    
    // Change circle color and members when clicked
    $(".circle").live("click", function(event) {
        if ($(this).attr("id") != "newCircle")
        {
            $(".selectedCircle").removeClass("selectedCircle");
            $(this).addClass("selectedCircle");
        
            if ($(this).attr("id") != "newCircle")
            {
                var circleID = parseInt($(this).attr("circleID"));
                var circleName = $(this).val()
                
                $.ajax({
                    type: "POST",
                    url: "/inkle/circleContent/",
                    data: { "circleID" : circleID },
                    success: function(html) {
                        $("#circleContent").fadeOut("medium", function() {
                            $("#circleContent").html(html);
                            $("#addToCircleInput").val("Add people to this circle");
                            $("#circleContent").fadeIn("medium");
                        });
                        
                    },
                    error: function(a, b, error) { alert(error); }
                });
            }
        }
    });

    $(".circle").live("mouseenter", function() {
        $(this).css("border", "solid 5px #009ACD");
    });
    $(".circle").live("mouseleave", function() {
        $(this).css("border", "solid 5px #CCC");
    });
    $("#createCircleButton").live("mouseenter", function() {
        $(this).css("border", "solid 5px #009ACD");
    });
    $("#createCircleButton").live("mouseleave", function() {
        $(this).css("border", "solid 5px #CCC");
    });

    $("#createCircleButton").live("click", function() {
        $(this).before("<button id='newCircle' class='circle'><input id='newCircleInput' type='text' /></button>");
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
                url: "/inkle/createCircle/",
                data: { "circleName" : newCircleName },
                success: function(circleID) {
                    $("#newCircle").attr("circleID", circleID);
                    $("#newCircle").removeAttr("id");
                    $(".circle").each(function() {
                        if ($(this).hasClass("selectedCircle")) {
                            $(this).trigger("click");
                        }
                    })
                },
                error: function(a, b, error) { alert(error); }
            });
            $("#newCircle").html(newCircleName);
        }
        $("#createCircleButton").show();
    });

    $("#deleteCircleButton").live("click", function() {

        $.ajax({
            type: "POST",
            url: "/inkle/deleteCircle/",
            data: { "circleID" : parseInt($(this).attr("circleID")) },
            success: function() {
                $.ajax({
                    type: "POST",
                    url: "/inkle/circles/",
                    data: {},
                    success: function(html) {
                        $("#primaryContent").html(html);
                    },
                    error: function(a, b, error) { alert(error); }
                });
            },
            error: function(a, b, error) { alert(error); }
        });
    });

    $("#addToCircleInput").live("keyup", function(e) {
        var query = $("#addToCircleInput").val();
        var circleID = parseInt($(this).attr("circleID"));

        if (query != "")
        {
            $.ajax({
                type: "POST",
                url: "/inkle/suggestions/",
                data: {"type" : "addToCircle", "circleID" : circleID, "query" : query},
                success: function(html) {
                    $("#addToCircleSuggestions").html(html);
                    $("#addToCircleSuggestions").fadeIn("medium");
                },
                error: function(a, b, error) { alert(error); }
            });
        }
        else
        {
            $("#addToCircleSuggestions").fadeOut("medium");
        }
    });
    
    $("#addToCircleSuggestions .suggestion").live("click", function() {
        var toMemberID = $(this).attr("suggestionID");
        var circleID = parseInt($("#addToCircleInput").attr("circleID"));

        $.ajax({
            type: "POST",
            url: "/inkle/addToCircle/",
            data: {"circleID" : circleID, "toMemberID" : toMemberID},
            success: function(html) {
                $("#circleMembers").prepend(html);
                $("#addToCircleInput").val("");
                $("#addToCircleSuggestions").fadeOut("medium");
            },
            error: function(a, b, error) { alert(error); }
        });
    });
    
    $("#addToCircleInput").live("blur", function() {
        $("#addToCircleSuggestions").fadeOut("medium");
    });
});
