$(document).ready(function() {
    $("#dinnerInklingInput").val("");
    
    $("#dinnerInklingInput").keyup(function(e) {
        var query = $("#dinnerInklingInput").val();
        
        if (query != "")
        {
            $.ajax({
                type: "POST",
                url: "/inkle/suggestions/",
                data: {"type" : "inkling", "query" : query},
                success: function(html) {
                    $("#dinnerInklingSuggestions").html(html);
                    $("#dinnerInklingSuggestions").fadeIn("medium");
                },
                error: function(a, b, error) { alert(error); }
            });
        }
        else
        {
            $("#dinnerInklingSuggestions").fadeOut("medium");
        }
    });
});
