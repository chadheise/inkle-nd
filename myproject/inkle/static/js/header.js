$(document).ready(function() {
    /* Initially, make the search input says "Search" and gray it out */
    $("#searchInput").val("Search").addClass("emptySearchInput");
    
    /* If the search input gains focus and it says "Search" grayed out, make the text black and empty it */
    $("#searchInput").focus(function() {
        if ($(this).hasClass("emptySearchInput"))
        {
            $(this).val("").removeClass("emptySearchInput");
        }
    });
   
    /* If the search input loses focus and is empty, gray it out and put "Search" in it  and fade out the search suggestions*/
    $("#searchInput").blur(function() {
        if ($(this).val() == "")
        {
            $(this).val("Search").addClass("emptySearchInput");
        }
        
        $("#searchSuggestions").fadeOut("medium");
    });

    $("#searchInput").keydown(function(e) {
        if ((e.keyCode == 10) || (e.keyCode == 13))
        {
            var query = $("#searchInput").val();
            query = query.replace(/^\s+|\s+$/g, "");

            if (query != "")
            {
                window.location.href = "/search/" + query;
            }
        }
    });
    
    $("#searchInput").keyup(function(e) {
        if ((e.keyCode != 10) && (e.keyCode != 13))
        {
            var query = $("#searchInput").val();

            if (query != "")
            {
                $.ajax({
                    type: "POST",
                    url: "/suggestions/",
                    data: {"type" : "search", "query" : query},
                    success: function(html) {
                        $("#searchSuggestions").html(html);
                        $("#searchSuggestions").fadeIn("medium");
                    },
                    error: function(a, b, error) {
                        ;
                        //alert("header.js (1): " + error);
                    }
                });
            }
            else
            {
                $("#searchSuggestions").fadeOut("medium");
            }
        }
    });
    
    $("#searchSuggestions .suggestion").live("click", function() {
        var query = $(this).children(".suggestion p").text();
        window.location.href = "/search/" + query;
    });
});
