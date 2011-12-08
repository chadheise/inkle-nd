$(document).ready(function() {
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
});
