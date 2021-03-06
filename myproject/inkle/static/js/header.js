/* Copyright 2012 Chad Heise & Jacob Wenger - All Rights Reserved */

$(document).ready(function() {
    /* Initially, make the search input says "Search" and gray it out */
    $("#headerSearchInput").val("Search for people, locations, and networks").addClass("emptySearchInput");
    
    /* If the search input gains focus and it says "Search" grayed out, make the text black and empty it */
    $("#headerSearchInput").focus(function() {
        if ($(this).hasClass("emptySearchInput"))
        {
            $(this).val("").removeClass("emptySearchInput");
        }
    });
   
    /* If the search input loses focus and is empty, gray it out, put "Search" in it, and fade out the search suggestions*/
    $("#headerSearchInput").blur(function() {
        if ($(this).val() == "")
        {
            $(this).val("Search for people, locations, and networks").addClass("emptySearchInput");
        }
        
        $("#headerSearchSuggestions").fadeOut("medium");
    });

    $("#headerSearchSuggestions .suggestion").live("hover", function() {
        // If there is a selected item, remove it
        if ($(".selectedSuggestion").length != 0)
        {
            $(".selectedSuggestion").removeClass("selectedSuggestion");
        }

        // Set the suggestion which was hovered over as selected
        $(this).addClass("selectedSuggestion");
    });

    /* If the "Enter" button is pressed and the search input is not empty, redirect to the search page */
    $("#headerSearchInput").keyup(function(e) {
        // Get the current search query and strip its whitespace
        var query = $(this).val().replace(/^\s+|\s+$/g, "");

        // Make sure the search query is not empty
        if (query != "")
        {
            // If the "Enter" button is pressed, redirect to the search page or trigger the selected item's click event
            if ((e.keyCode == 10) || (e.keyCode == 13))
            {
                // If there is no selected item, redirect to the search page with the current query
                if ($(".selectedSuggestion").length == 0)
                {
                    window.location.href = "/search/" + query;
                }

                // Otherwise, trigger the selected item's click event
                else
                {
                    window.location.href = $(".selectedSuggestion").parent().attr("href");
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
                    var nextSuggestionElement = selectedSuggestionElement.parent().prev().find(".suggestion");
                    selectedSuggestionElement.removeClass("selectedSuggestion");
                    nextSuggestionElement.addClass("selectedSuggestion");
                    if ($(".selectedSuggestion").length == 0)
                    {
                        var nextSuggestionElement = selectedSuggestionElement.parent().prev().prev().find(".suggestion");
                        nextSuggestionElement.addClass("selectedSuggestion");
                    }
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
                    var nextSuggestionElement = selectedSuggestionElement.parent().next().find(".suggestion");
                    selectedSuggestionElement.removeClass("selectedSuggestion");
                    nextSuggestionElement.addClass("selectedSuggestion");
                    if ($(".selectedSuggestion").length == 0)
                    {
                        var nextSuggestionElement = selectedSuggestionElement.parent().next().next().find(".suggestion");
                        nextSuggestionElement.addClass("selectedSuggestion");
                    }
                }
            }

            // Otherwise, if the left or right arrow keys are not pressed, update the search suggestions
            else if ((e.keyCode != 37) && (e.keyCode != 39))
            {
                $.ajax({
                    type: "POST",
                    url: "/suggestions/",
                    data: {"type" : "search", "query" : query},
                    success: function(html) {
                        $("#headerSearchSuggestions").html(html);
                        $("#headerSearchSuggestions").fadeIn("medium");
                    },
                    error: function(jqXHR, textStatus, error) {
                        if ($("body").attr("debug") == "True")
                        {
                            alert("header.js (1): " + error);
                        }
                    }
                });
            }
        }

        // If the search query is empty, fade out the search suggestions
        else
        {
            $("#headerSearchSuggestions").fadeOut("medium");
        }
    });
    
    /* If the search button is clicked and the search input is not empty, redirect to the search page */
    $("#headerSearchButton").click(function() {
        var query = $("#headerSearchInput").val();
        query = query.replace(/^\s+|\s+$/g, "");

        if ((query != "") && (!$("#headerSearchInput").hasClass("emptySearchInput")))
        {
            window.location.href = "/search/" + query;
        }
    });
   
    /* Fades in the header dropdown menu when the header dropdown menu button is clicked */
    $("#headerDropdownButton").live("click", function() {
        // Get the header dropdown menu
        var headerDropdownElement = $("#headerDropdown");
       
        // If the header dropdown menu is not visible, fade it in
        if (! headerDropdownElement.is(":visible"))
        {
            var buttonPosition = $(this).position();
            var buttonHeight = $(this).height();
            var buttonWidth = $(this).width();
            headerDropdownElement
                .css("left", buttonPosition.left + 20 - headerDropdownElement.width())
                .css("top", (buttonPosition.top + 2 * buttonHeight + 22))
                .fadeIn("medium");
            $(this).addClass("selectedHeaderDropdownButton");
        }

        // Otherwise, if the blots menu is visible, fade it out
        else
        {
            headerDropdownElement.fadeOut("medium");
            $(this).removeClass("selectedHeaderDropdownButton");
        }
    });
    
    /* Fades out the header dropdown menu when a click occurs on an element which is not part of the header dropdown menu */
    $("html").live("click", function(e) {
        if ($("#headerDropdown:visible").length != 0)
        {
            if ((!($(e.target).hasClass("headerDropdownOption"))) && (e.target.id != "headerDropdownButton") && (($(e.target).parents("#headerDropdown").length == 0)))
            {
                $("#headerDropdown").fadeOut("fast");
                $("#headerDropdownButton").removeClass("selectedHeaderDropdownButton");
            }
        }
    });

    /* Redirect to the search page when the header search's more suggestions link is clicked */
    $("#headerSearch #moreSuggestions").live("click", function() {
        var query = $(this).children(".suggestion p").text();
        window.location.href = "/search/" + query;
    });

    /* FOOTER STUFF */
    /* Fades in the invite your friends content when the "Invite your friends" button is clicked */
    $("#inviteYourFriendsButton").live("click", function() {
        // Get the invite your friends content
        var inviteYourFriendsElement = $("#inviteYourFriendsContent");
       
        // If the invite your friends content is not visible, fade it in
        if (! inviteYourFriendsElement.is(":visible"))
        {
            var buttonPosition = $(this).position();
            var buttonHeight = $(this).height();
            var buttonWidth = $(this).width();
            inviteYourFriendsElement
                .css("right", buttonPosition.left - 59)
                .css("bottom", buttonPosition.top + 26)
                .fadeIn("medium");
            $(this).addClass("selectedInviteYourFriendsButton");
        }

        // Otherwise, if the invite your friends element is visible, fade it out
        else
        {
            inviteYourFriendsElement.fadeOut("medium");
            $(this).removeClass("selectedInviteYourFriendsButton");
        }
    });
    
    /* Fades out the header dropdown menu when a click occurs on an element which is not part of the header dropdown menu */
    $("html").live("click", function(e) {
        if ($("#inviteYourFriendsContent:visible").length != 0)
        {
            if ((e.target.id != "inviteYourFriendsContent") && (e.target.id != "inviteYourFriendsButton") && (($(e.target).parents("#inviteYourFriendsContent").length == 0)))
            {
                $("#inviteYourFriendsContent").fadeOut("medium");
                $("#inviteYourFriendsButton").removeClass("selectedInviteYourFriendsButton");
            }
        }
    });

    $("#inviteYourFriendsContent textarea").addClass("emptyTextarea");
    
    /* If the search input gains focus and it says "Search" grayed out, make the text black and empty it */
    $("#inviteYourFriendsContent textarea").focus(function() {
        if ($(this).hasClass("emptyTextarea"))
        {
            $(this).val("").removeClass("emptyTextarea");
        }
    });
   
    /* If the search input loses focus and is empty, gray it out, put "Search" in it, and fade out the search suggestions*/
    $("#inviteYourFriendsContent textarea").blur(function() {
        if ($(this).val() == "")
        {
            $(this).val("Invite your friends to join Inkle by typing their email addresses here").addClass("emptyTextarea");
        }
        
        $("#headerSearchSuggestions").fadeOut("medium");
    });

    $("#inviteToInkleSendButton").live("click", function() {
        var emails = $("#inviteYourFriendsContent textarea").val();

        $.ajax({
            type: "POST",
            url: "/inviteToInkle/",
            data: { "emails" : emails },
            success: function() {
                $("#inviteYourFriendsContent textarea").val("Thank you for telling your friends about Inkle!").addClass("emptyTextarea");
            },
            error: function(jqXHR, textStatus, error) {
                if ($("body").attr("debug") == "True")
                {
                    alert("header.js (2): " + error);
                }
            }
        });
    });

});
