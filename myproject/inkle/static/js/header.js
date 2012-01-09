$(document).ready(function() {
    /* Initially, make the search input says "Search" and gray it out */
    $("#headerSearchInput").val("Search").addClass("emptySearchInput");
    
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
            $(this).val("Search").addClass("emptySearchInput");
        }
        
        $("#headerSearchSuggestions").fadeOut("medium");
    });

    /* If the "Enter" button is pressed and the search input is not empty, redirect to the search page */
    $("#headerSearchInput").keydown(function(e) {
        if ((e.keyCode == 10) || (e.keyCode == 13))
        {
            var query = $(this).val();
            query = query.replace(/^\s+|\s+$/g, "");

            if (query != "")
            {
                window.location.href = "/search/" + query;
            }
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
   
    /* Update the search suggestions every time a key is pressed */
    $("#headerSearchInput").keyup(function(e) {
        if ((e.keyCode != 10) && (e.keyCode != 13))
        {
            var query = $(this).val();

            if (query != "")
            {
                $.ajax({
                    type: "POST",
                    url: "/suggestions/",
                    data: {"type" : "search", "query" : query},
                    success: function(html) {
                        $("#headerSearchSuggestions").html(html);
                        $("#headerSearchSuggestions").fadeIn("medium");
                    },
                    error: function(a, b, error) {
                        ;
                        alert("header.js (1): " + error);
                    }
                });
            }
            else
            {
                $("#headerSearchSuggestions").fadeOut("medium");
            }
        }
    });

    /* Every time a search suggestion is clicked, redirect to the search page */
    $("#headerSearchSuggestions .suggestion").live("click", function() {
        var query = $(this).children(".suggestion p").text();
        window.location.href = "/search/" + query;
    });
});
