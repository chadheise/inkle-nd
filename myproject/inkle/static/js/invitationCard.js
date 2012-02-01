$(document).ready(function() {
    /* Accept the clicked inviation when an "Accept invitation" button is clicked */
    $(".acceptInvitation").live("click", function() {
        var invitationCard = $(this).parents(".invitationCard");
        var invitationID = parseInt($(this).attr("invitationID"));

        // Accept the inkling invitations
        $.ajax({
            type: "POST",
            url: "/invitationResponse/",
            data: { "invitationID" : invitationID, "response" : "accept" },
            success: function(html) {
            },
            error: function(a, b, error) { alert("invitationCard.js (1): " + error); }
        });
    });

    /* Reject the clicked invitation when a "Reject invitation" button is clicked */
    $(".rejectInvitation").live("click", function() {
        var invitationCard = $(this).parents(".invitationCard");
        var invitationID = parseInt($(this).attr("invitationID"));

        // Accept the inkling invitations
        $.ajax({
            type: "POST",
            url: "/invitationResponse/",
            data: { "invitationID" : invitationID, "response" : "reject" },
            success: function(html) {
            },
            error: function(a, b, error) { alert("invitationCard.js (2): " + error); }
        });
    });
});
