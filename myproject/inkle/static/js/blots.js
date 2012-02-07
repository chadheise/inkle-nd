$(document).ready(function() {
    /* Update the selected blot and the blot content when a blot is clicked */
    $(".blot").live("click", function(event) {
        // Only do this if the blot which was clicked is not the new blot or the currently selected blot
        if (($(this).attr("id") != "newBlot") && (!$(this).hasClass("selectedBlot")))
        {
            // Set the clicked blot and the selected blot
            $(".selectedBlot").removeClass("selectedBlot");
            $(this).addClass("selectedBlot");

            // Get the clicked blots ID
            var blotID = parseInt($(this).attr("blotID"));

            // If the selected blot's ID is -1 (i.e. the accepted blot), set the URL with no blot ID
            if (blotID == -1)
            {
                url = "/blots/";
            }

            // Otherwise, put the blot ID in the URL
            else
            {
                url = "/blots/" + blotID + "/";
            }

            // Load the blot's content
            $.ajax({
                type: "POST",
                url: url,
                data: { "content" : "blotOnly" },
                success: function(html) {
                    $("#blotContent").fadeOut("medium", function() {
                        $("#blotContent").html(html);
                        $("#addToBlotInput").val("Add people to this blot").addClass("emptyAddToBlotInput");
                        $("#blotContent").fadeIn("medium");
                    });
                },
                error: function(a, b, error) { alert("blots.js (1): " + error); }
            });
        }
    });
    
    /* Update a blot's name when it is double clicked */
    $(".blot").live("dblclick", function() {
        // Only do this if the blot which was clicked is not the new blot
        if (($(this).attr("id") != "newBlot") && ($(this).attr("blotID") != -1))
        {
            // Set the clicked blot and the selected blot
            var currentBlotName = $(this).text();
            $(this).html("<input id='renameBlotInput' type='text' value='" + currentBlotName + "' maxlength='50' />");
            $("#renameBlotInput").focus();
        }
    });

    /* Renames the blot with the inputted ID to the inputted name */
    function renameBlot(blotID, blotName)
    {
        $.ajax({
            type: "POST",
            url: "/renameBlot/",
            data: { "blotID" : blotID, "blotName" : blotName },
            success: function(html) {
                var blot = $("#renameBlotInput").parent(".blot");
                blot.html("<p>" + blotName + "</p>");
                var blotP = blot.find("p");
                var marginTop = (blot.height() - blotP.height()) / 2;
                blot.find("p").css("margin-top", marginTop + "px");

            },
            error: function(a, b, error) { alert("blots.js (1): " + error); }
        });
    }

    /* Renames the blot with the rename blot input when the rename blot input loses focus */
    $("#renameBlotInput").live("blur", function() {
        // Get the ID of the blot whose name is being changed
        var blotID = parseInt($("#renameBlotInput").parent(".blot").attr("blotID"));
        var newBlotName = $("#renameBlotInput").val();
                
        // Change the blot's name and hide the rename blot input
        renameBlot(blotID, newBlotName);
    });
    
    /* Renames the blot with the rename blot input when the rename blot input loses focus */
    $("#renameBlotInput").live("keypress", function(e) {
        if ((e.keyCode == 10) || (e.keyCode == 13))
        {
            // Get the ID of the blot whose name is being changed
            var blotID = parseInt($("#renameBlotInput").parent(".blot").attr("blotID"));
            var newBlotName = $("#renameBlotInput").val();
                
            // Change the blot's name and hide the rename blot input
            renameBlot(blotID, newBlotName);
        }
    });

    /* Change the text for the add to blot input when it gains focus */
    $("#addToBlotInput").live("focus", function() {
        if ($(this).hasClass("emptyAddToBlotInput"))
        {
            $(this).val("").removeClass("emptyAddToBlotInput");
        }
    });
    
    /* Change the text for the add to blot input when it loses focus */
    $("#addToBlotInput").live("blur", function() {
        if ($(this).val() == "")
        {
            $(this).val("Add people to this blot").addClass("emptyAddToBlotInput");
        }
    });
    
    /* Displays the new blot when the create blot button is clicked */
    $("#createBlotButton").live("click", function() {
        $(this).fadeOut("medium", function() {
            $("#newBlot").fadeIn("medium");
            $("#newBlotInput").focus();
        });
    });

    /* Creates a new blot */
    function createBlot(name)
    {
        // If the blot name is empty, don't create a new blot and fade in the create blot button
        if (name == "")
        {
            $("#newBlot").fadeOut("medium", function() {
                $("#createBlotButton").fadeIn("medium");
            });
        }

        // Otherwise, create a new blot with the inputted name
        else
        {
            $.ajax({
                type: "POST",
                url: "/createBlot/",
                data: { "blotName" : name },
                success: function(blotID) {
                    $("#newBlot").fadeOut("medium", function() {
                        $("#newBlotInput").val("");
                        var blot = $("<div class='blot' blotID='" + blotID + "'><p>" + name + "</p></div>");
                        $("#newBlot").before(blot);
                        var blotP = blot.find("p");
                        var marginTop = (blot.height() - blotP.height()) / 2;
                        blot.find("p").css("margin-top", marginTop + "px");
                        $(".blotsMenu").each( function() {
                            memberID = $(this).siblings(".cardButton").attr("memberID")
                            $(this).append("<div><input id='m" + memberID + "_c" + blotID + "' type='checkbox' blotID='" +  blotID + "' /> <label for='m" + memberID + "_c" + blotID + "'>" + name + "</label></div>");
                            $(".noBlots").remove()
                        });
                        $("#createBlotButton").fadeIn("medium");
                    });
                },
                error: function(a, b, error) { alert("blots.js (2): " + error); }
            });
        }
    }

    /* Create a new blot when the new blot input loses focus */
    $("#newBlotInput").live("blur", function() {
        createBlot($("#newBlotInput").val());
    });

    /* Create a new blot when the enter button is pressed in the blot input */
    $("#newBlotInput").live("keypress", function(e) {
        if ((e.keyCode == 10) || (e.keyCode == 13))
        {
            createBlot($("#newBlotInput").val());
        }
    });

    /* Deletes the currently selected blot */
    $("#deleteBlotButton").live("click", function() {
        // Get the ID of the currently selected blot
        var blotID = parseInt($(".selectedBlot").attr("blotID"))

        // Delete the currently selected blot and set the accepted blot as the newly selected blot
        $.ajax({
            type: "POST",
            url: "/deleteBlot/",
            data: { "blotID" : blotID },
            success: function() {
                $(".selectedBlot").fadeOut("medium", function() {
                    $(".blot:first").trigger("click");
                });
            },
            error: function(a, b, error) { alert("blots.js (4): " + error); }
        });
    });

    $("#addToBlotSuggestions .suggestion").live("hover", function() {
        // If there is a selected item, remove it
        if ($(".selectedSuggestion").length != 0)
        {
            $(".selectedSuggestion").removeClass("selectedSuggestion");
        }

        // Set the suggestion which was hovered over as selected
        $(this).addClass("selectedSuggestion");
    });

    $("#addToBlotInput").live("keyup", function(e) {
        var query = $("#addToBlotInput").val();
        var blotID = parseInt($(this).attr("blotID"));

        if (query != "")
        {
            // If the "Enter" button is pressed, redirect to the search page or trigger the selected item's click event
            if ((e.keyCode == 10) || (e.keyCode == 13))
            {
                // Otherwise, trigger the selected item's click event
                if ($(".selectedSuggestion").length != 0)
                {
                    $(".selectedSuggestion").trigger("click");
                }
            }

            // If the up arrow key is pressed, scroll through the suggestions
            else if (e.keyCode == 38)
            {
                // If there is no selected suggestion, set the last suggestion as selected
                if ($(".selectedSuggestion").length == 0)
                {
                    $(".suggestion:last").addClass("selectedSuggestion");
                }

                // Otherwise, set the previous suggestion as selected
                else
                {
                    var selectedSuggestionElement = $(".selectedSuggestion");
                    var nextSuggestionElement = selectedSuggestionElement.prev();
                    selectedSuggestionElement.removeClass("selectedSuggestion");
                    nextSuggestionElement.addClass("selectedSuggestion");
                }
            }
       
            // If the down arrow key is pressed, scroll through the suggestions
            else if (e.keyCode == 40)
            {
                // If there is no selected suggestion, set the first suggestion as selected
                if ($(".selectedSuggestion").length == 0)
                {
                    $(".suggestion:first").addClass("selectedSuggestion");
                }

                // Otherwise, set the next suggestion as selected
                else
                {
                    var selectedSuggestionElement = $(".selectedSuggestion");
                    var nextSuggestionElement = selectedSuggestionElement.next();
                    selectedSuggestionElement.removeClass("selectedSuggestion");
                    nextSuggestionElement.addClass("selectedSuggestion");
                }
            }

            // Otherwise, if the left or right arrow keys are not pressed, update the search suggestions
            else if ((e.keyCode != 37) && (e.keyCode != 39))
            {
                $.ajax({
                    type: "POST",
                    url: "/suggestions/",
                    data: { "type" : "addToBlot", "blotID" : blotID, "query" : query },
                    success: function(html) {
                        $("#addToBlotSuggestions").html(html);
                        $("#addToBlotSuggestions").fadeIn("medium");
                    },
                    error: function(a, b, error) { alert("blots.js (5): " + error); }
                });
            }
        }
        else
        {
            $("#addToBlotSuggestions").fadeOut("medium");
        }
    });
    
    $("#addToBlotSuggestions .suggestion").live("click", function() {
        var toMemberID = $(this).attr("suggestionID");
        var blotID = parseInt($("#addToBlotInput").attr("blotID"));

        $.ajax({
            type: "POST",
            url: "/addToBlot/",
            data: {"blotID" : blotID, "toMemberID" : toMemberID},
            success: function(html) {
                if ($("#blotMembers .memberCard").length == 0)
                {
                    $("#blotMembers").html("");
                }
                $("#blotMembers").prepend(html);
                $(".blotsMenu").each( function() {
                    memberID = $(this).siblings(".cardButton").attr("memberID")
                    $(".noBlots").remove()
                });
                $("#addToBlotInput").val("");
                $("#addToBlotSuggestions").fadeOut("medium");
            },
            error: function(a, b, error) { alert("blots.js (6): " + error); }
        });
    });
    
    $("#addToBlotInput").live("blur", function() {
        $("#addToBlotSuggestions").fadeOut("medium");
    });
});
