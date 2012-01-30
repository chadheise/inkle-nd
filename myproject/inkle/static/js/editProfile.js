$(document).ready(function() {
    // Populate the main content with the initially selected main content link
    var contentType = $("#editProfileContentLinks .selectedContentLink").attr("contentType");
    loadContent(contentType, true);

    /* Loads the content for the inputted content type and populates the main content with it */
    function loadContent(contentType, firstLoad)
    {
        $.ajax({
            type: "POST",
            url: "/" + contentType + "/",
            data: {},
            success: function(html) {
                // If this is the first load, simply load the edit profile content
                if (firstLoad)
                {
                    loadContentHelper(html, contentType);
                }

                // Otherwise, fade out the current edit profile content and fade the new edit profile content back in
                else
                {
                    $("#editProfileContent").fadeOut("medium", function () {
                        loadContentHelper(html, contentType, function() {
                            $("#editProfileContent").fadeIn("medium");
                        });
                    });
                }
            },
            error: function(a, b, error) { alert("editProfile.js (1): " + error); }
        });
    }
 
    /* Helper function for loadContent() which replaces the edit profile content HTML*/
    function loadContentHelper(html, contentType, callback)
    {
        // Update the main content with the HTML returned from the AJAX call
        $("#editProfileContent").html(html);

        // Execute the callback function if there is one
        if (callback)
        {
            callback();
        }
    }

    /* Updates the main content when one of the main content links is clicked */
    $("#editProfileContentLinks p").click(function() {
        // Only update the content if the main content link which is clicked is not the currently selected one
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Update the selected main content link
            $("#editProfileContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Load the content for the clicked main content link
            var contentType = $(this).attr("contentType");
            loadContent(contentType, false);
        }
    });

    /* Define a startsWith() string function */
    if(!String.prototype.startsWith) {
        String.prototype.startsWith = function (str) {
            return !this.indexOf(str);
        }
    }

    $("#editProfileInformationButton").live("click", function() {
        var firstName = $("#firstName").val();
        var lastName = $("#lastName").val();
        var phone1 = $("#phone1").val();
        var phone2 = $("#phone2").val();
        var phone3 = $("#phone3").val();
        var city = $("#city").val();
        var state = $("#state option:selected").val(); 
        var zipCode = $("#zipCode").val();
        var month = $("#month option:selected").val(); 
        var day = $("#day option:selected").val(); 
        var year = $("#year option:selected").val(); 
        var gender = $("#gender option:selected").val(); 

        $.ajax({
            type: "POST",
            url: "/editProfileInformation/",
            data: { "firstName" : firstName, "lastName" : lastName, "phone1" : phone1, "phone2" : phone2, "phone3" : phone3, "city" : city, "state" : state, "zipCode" : zipCode, "month" : month, "day" : day, "year" : year, "gender" : gender },
            success: function(html) {
                if (html.startsWith("\n"))
                {
                    $("#editProfileContent").html(html);
                }
                else
                {
                    $(".invalid").removeClass("invalid");
                    $(".errors").remove();
                    $("#editProfileInformationContent").fadeOut("medium", function() {
                        $("#editProfileInformationConfirmation").fadeIn("medium").delay(2000).fadeOut("medium", function() {
                            $("#editProfileInformationContent").fadeIn("medium");
                        });
                    });
                }
            },
            error: function(a, b, error) { alert("editProfile.js (2): " + error); }
        });
    });
   
    /* Edit the logged in member's profile privacy settings when the "Edit profile privacy" button is clicked */
    $("#editProfilePrivacyButton").live("click", function() {
        // Get the privacy settings
        var locationPrivacy = $("#locationPrivacy option:selected").val(); 
        var emailPrivacy = $("#emailPrivacy option:selected").val(); 
        var phonePrivacy = $("#phonePrivacy option:selected").val(); 
        var birthdayPrivacy = $("#birthdayPrivacy option:selected").val(); 
        var followersPrivacy = $("#followersPrivacy option:selected").val(); 
        var followingsPrivacy = $("#followingsPrivacy option:selected").val(); 
        var spheresPrivacy = $("#spheresPrivacy option:selected").val(); 
        var inklingsPrivacy = $("#inklingsPrivacy option:selected").val(); 

        // Edit the logged in member's profile privacy settings
        $.ajax({
            type: "POST",
            url: "/editProfilePrivacy/",
            data: { "locationPrivacy" : locationPrivacy, "emailPrivacy" : emailPrivacy, "phonePrivacy" : phonePrivacy, "birthdayPrivacy" : birthdayPrivacy, "followersPrivacy" : followersPrivacy, "followingsPrivacy" : followingsPrivacy, "spheresPrivacy" : spheresPrivacy, "inklingsPrivacy" : inklingsPrivacy },
            success: function(html) {
                // Fade out the privacy content, fade in the confirmation message, and fade back in the privacy content after a delay
                $("#editProfilePrivacyContent").fadeOut("medium", function() {
                    $("#editProfilePrivacyConfirmation").fadeIn("medium").delay(2000).fadeOut("medium", function() {
                        $("#editProfilePrivacyContent").fadeIn("medium");
                    });
                });
            },
            error: function(a, b, error) { alert("editProfile.js (3): " + error); }
        });
    });

    /* Edit the logged in member's email preferences when the "Edit email preferences" button is clicked */
    $("#editProfileEmailPreferencesButton").live("click", function() {
        // Get the email preferences
        var requestedPreference = $("#requestedPreference").is(":checked"); 
        var acceptedPreference = $("#acceptedPreference").is(":checked"); 
        var invitedPreference = $("#invitedPreference").is(":checked"); 
        var generalPreference = $("#generalPreference").is(":checked"); 

        // Edit the logged in member's email preferences settings
        $.ajax({
            type: "POST",
            url: "/editProfileEmailPreferences/",
            data: { "requestedPreference" : requestedPreference, "acceptedPreference" : acceptedPreference, "invitedPreference" : invitedPreference, "generalPreference" : generalPreference, }, 
            success: function(html) {
                // Fade out the email preferences content, fade in the confirmation message, and fade back in the email preferences content after a delay
                $("#editProfileEmailPreferencesContent").fadeOut("medium", function() {
                    $("#editProfileEmailPreferencesConfirmation").fadeIn("medium").delay(2000).fadeOut("medium", function() {
                        $("#editProfileEmailPreferencesContent").fadeIn("medium");
                    });
                });
            },
            error: function(a, b, error) { alert("editProfile.js (7): " + error); }
        });
    });

    /* Make the iframe the target of the "Edit profile picture" button */
    $("#editProfilePictureForm").live("submit", function() {
        $("#editProfilePictureForm").attr("target", "uploadTarget");
    });

    /* Edit the logged in member's profile picture when the "Edit profile picture" button is clicked */
    $("#editProfilePictureButton").live("click", function() {
        if ($("#newProfilePicture").val())
        {
            $("#newProfilePicture").css("border", "solid 2px #BBB");

            // Fade out the profile picture content, fade in the confirmation message and update the profile picture, and fade back in the profile picture content after a delay
            $("#editProfilePictureContent").fadeOut("medium", function() {
                // Reload the member images
                var date = new Date()
                var imageSource = $("#headerMemberImage").attr("src") + "?" + date.getTime();
                $("#currentMemberImage").attr("src", imageSource);
                $("#headerMemberImage").attr("src", imageSource);


                $("#editProfilePictureConfirmation").fadeIn("medium").delay(2000).fadeOut("medium", function() {
                    $("#editProfilePictureContent").fadeIn("medium", function() {
                });
            
                });
            });
        }
        else
        {
            $("#newProfilePicture").css("border", "solid 2px #FF0000");
        }
    });
});
