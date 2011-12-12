$(document).ready(function() {
    $("#searchInput").val("Search");
    
    $("#searchInput").focus(function() {
        if ($(this).val() == "Search")
        {
            $(this).val("");
            $(this).css("color", "#000");
        }
    });
    
    $("#searchInput").blur(function() {
        if ($(this).val() == "")
        {
            $(this).val("Search");
            $(this).css("color", "#888");
        }
        
        $("#searchSuggestions").fadeOut("medium");
    });

    $("#searchInput").keydown(function(e) {
        if ((e.keyCode == 10) || (e.keyCode == 13))
        {
            var query = $("#searchInput").val();

            if (query != "")
            {
                window.location.href = "/inkle/search/" + query;
            }
        }
    });
    
    $("#searchInput").keyup(function(e) {
        var query = $("#searchInput").val();

        if (query != "")
        {
            $.ajax({
                type: "POST",
                url: "/inkle/suggestions/",
                data: {"type" : "search", "query" : query},
                success: function(html) {
                    $("#searchSuggestions").html(html);
                    $("#searchSuggestions").fadeIn("medium");
                },
                error: function(a, b, error) { alert(error); }
            });
        }
        else
        {
            $("#searchSuggestions").fadeOut("medium");
        }
    });
    
    $("#searchSuggestions .suggestion").live("click", function() {
        var query = $(this).children(".suggestionText").text();
        window.location.href = "/inkle/search/" + query;
    });
    
    $("#requestNotification").live("click", function() {
            window.location.href = "/inkle/manage/requests";
            
            //$(this).post("inkle/manage/", {defaultContent : "requests"});
/*
            $.ajax({
                type: "POST",
                url: "/inkle/manage/",
                data: {defaultContent : "requests"},
                success: function() { alert("sucessful call");},
                error: function(a, b, error) { alert(error); }
            });*/

        });

    $("#requestNotification").live("mouseenter", function() {
        $(this).css("border", "solid 1px darkred");
        $(this).css("cursor", "pointer");
    });
    
    $("#requestNotification").live("mouseleave", function() {
        $(this).css("border", "none");
    });
    
    
});
