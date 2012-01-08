$(document).ready(function() {
    /* Update the selected circle and the circle content when a circle is clicked */
    $(".circle").live("click", function(event) {
        // Only do this if the circle which was clicked is not the new circle or the currently selected circle
        if (($(this).attr("id") != "newCircle") && (!$(this).hasClass("selectedCircle")))
        {
            // Set the clicked circle and the selected circle
            $(".selectedCircle").removeClass("selectedCircle");
            $(this).addClass("selectedCircle");

            // Get the clicked circles ID
            var circleID = parseInt($(this).attr("circleID"));

            // If the selected circle's ID is -1 (i.e. the accepted circle), set the URL with no circle ID
            if (circleID == -1)
            {
                url = "/circles/";
            }

            // Otherwise, put the circle ID in the URL
            else
            {
                url = "/circles/" + circleID + "/";
            }

            // Load the circle's content
            $.ajax({
                type: "POST",
                url: url,
                data: { "content" : "circleOnly" },
                success: function(html) {
                    $("#circleContent").fadeOut("medium", function() {
                        $("#circleContent").html(html);
                        $("#addToCircleInput").val("Add people to this circle").addClass("emptyAddToCircleInput");
                        $("#circleContent").fadeIn("medium");
                    });
                },
                error: function(a, b, error) { alert("circles.js (1): " + error); }
            });
        }
    });
    
    /* Update a circle's name when it is double clicked */
    $(".circle").live("dblclick", function() {
        // Only do this if the circle which was clicked is not the new circle
        if (($(this).attr("id") != "newCircle") && ($(this).attr("circleID") != -1))
        {
            // Set the clicked circle and the selected circle
            var currentCircleName = $(this).text();
            $(this).html("<input id='renameCircleInput' type='text' value='" + currentCircleName + "' maxlength='50' />");
            $("#renameCircleInput").focus();
        }
    });

    /* Renames the circle with the inputted ID to the inputted name */
    function renameCircle(circleID, circleName)
    {
        $.ajax({
            type: "POST",
            url: "/renameCircle/",
            data: { "circleID" : circleID, "circleName" : circleName },
            success: function(html) {
                $("#renameCircleInput").parent(".circle").html(circleName);
            },
            error: function(a, b, error) { alert("circles.js (1): " + error); }
        });
    }

    /* Renames the circle with the rename circle input when the rename circle input loses focus */
    $("#renameCircleInput").live("blur", function() {
        // Get the ID of the circle whose name is being changed
        var circleID = parseInt($("#renameCircleInput").parent(".circle").attr("circleID"));
        var newCircleName = $("#renameCircleInput").val();
                
        // Change the circle's name and hide the rename circle input
        renameCircle(circleID, newCircleName);
    });
    
    /* Renames the circle with the rename circle input when the rename circle input loses focus */
    $("#renameCircleInput").live("keypress", function(e) {
        if ((e.keyCode == 10) || (e.keyCode == 13))
        {
            // Get the ID of the circle whose name is being changed
            var circleID = parseInt($("#renameCircleInput").parent(".circle").attr("circleID"));
            var newCircleName = $("#renameCircleInput").val();
                
            // Change the circle's name and hide the rename circle input
            renameCircle(circleID, newCircleName);
        }
    });

    /* Change the text for the add to circle input when it gains focus */
    $("#addToCircleInput").live("focus", function() {
        if ($(this).hasClass("emptyAddToCircleInput"))
        {
            $(this).val("").removeClass("emptyAddToCircleInput");
        }
    });
    
    /* Change the text for the add to circle input when it loses focus */
    $("#addToCircleInput").live("blur", function() {
        if ($(this).val() == "")
        {
            $(this).val("Add people to this circle").addClass("emptyAddToCircleInput");
        }
    });
    
    /* Displays the new circle when the create circle button is clicked */
    $("#createCircleButton").live("click", function() {
        $(this).fadeOut("medium", function() {
            $("#newCircle").fadeIn("medium");
            $("#newCircleInput").focus();
        });
    });

    /* Creates a new circle */
    function createCircle(name)
    {
        // If the circle name is empty, don't create a new circle and fade in the create circle button
        if (name == "")
        {
            $("#newCircle").fadeOut("medium", function() {
                $("#createCircleButton").fadeIn("medium");
            });
        }

        // Otherwise, create a new circle with the inputted name
        else
        {
            $.ajax({
                type: "POST",
                url: "/createCircle/",
                data: { "circleName" : name },
                success: function(circleID) {
                    $("#newCircle").fadeOut("medium", function() {
                        $("#newCircleInput").val("")
                        $("#newCircle").before("<button class='circle' circleID='" + circleID + "'>" + name + "</button>");
                        $("#createCircleButton").fadeIn("medium");
                    });
                },
                error: function(a, b, error) { alert("circles.js (2): " + error); }
            });
        }
    }

    /* Create a new circle when the new circle input loses focus */
    $("#newCircleInput").live("blur", function() {
        createCircle($("#newCircleInput").val());
    });

    /* Create a new circle when the enter button is pressed in the circle input */
    $("#newCircleInput").live("keypress", function(e) {
        if ((e.keyCode == 10) || (e.keyCode == 13))
        {
            createCircle($("#newCircleInput").val());
        }
    });

    /* Deletes the currently selected circle */
    $("#deleteCircleButton").live("click", function() {
        // Get the ID of the currently selected circle
        var circleID = parseInt($(".selectedCircle").attr("circleID"))

        // Delete the currently selected circle and set the accepted circle as the newly selected circle
        $.ajax({
            type: "POST",
            url: "/deleteCircle/",
            data: { "circleID" : circleID },
            success: function() {
                $(".selectedCircle").fadeOut("medium", function() {
                    $(".circle:first").trigger("click");
                });
            },
            error: function(a, b, error) { alert("circles.js (4): " + error); }
        });
    });

    $("#addToCircleInput").live("keyup", function(e) {
        var query = $("#addToCircleInput").val();
        var circleID = parseInt($(this).attr("circleID"));

        if (query != "")
        {
            $.ajax({
                type: "POST",
                url: "/suggestions/",
                data: { "type" : "addToCircle", "circleID" : circleID, "query" : query },
                success: function(html) {
                    $("#addToCircleSuggestions").html(html);
                    $("#addToCircleSuggestions").fadeIn("medium");
                },
                error: function(a, b, error) { alert("circles.js (5): " + error); }
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
            url: "/addToCircle/",
            data: {"circleID" : circleID, "toMemberID" : toMemberID},
            success: function(html) {
                $("#circleMembers").prepend(html);
                $("#addToCircleInput").val("");
                $("#addToCircleSuggestions").fadeOut("medium");
            },
            error: function(a, b, error) { alert("circles.js (6): " + error); }
        });
    });
    
    $("#addToCircleInput").live("blur", function() {
        $("#addToCircleSuggestions").fadeOut("medium");
    });
});
