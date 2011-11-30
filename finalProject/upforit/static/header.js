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
});
