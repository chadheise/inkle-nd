$(document).ready(function() {
    $("#searchInput").focus(function() {
        var currentSearch = $("#searchInput").val();
        if (currentSearch == "Search")
        {
            $("#searchInput").val("");
            $("#searchInput").css("color", "#000");
        }
    });
    
    $("#searchInput").blur(function() {
        var currentSearch = $("#searchInput").val();
        if (currentSearch == "")
        {
            $("#searchInput").val("Search");
            $("#searchInput").css("color", "#888");
        }
    });
});
