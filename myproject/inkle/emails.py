from smtplib import SMTP_SSL
from email.mime.text import MIMEText

live = False

def send_email(from_address, to_addresses, subject, body_text, body_html):
    """Sends an email with the inputted details using the WebFaction SMTP server."""
    # Create the message
    # message = MIMEText(body_text)
    message = MIMEText(body_html, "html")
    message["Subject"] = subject

    # Connect to the server, send the email, and disconnect from the server
    server = SMTP_SSL("smtp.webfaction.com", 465)
    
    server.login("inkle", "AmiTabh-2012")

    if (not live):
        to_addresses = ["test@inkleit.com"]
    server.sendmail(from_address, to_addresses, message.as_string())

    server.quit()


def send_email_verification_email(member):
    """Sends the email verification email."""
    # Specify the from address and to addresses
    from_address = "inkle@inkleit.com"
    to_addresses = [member.email]

    # Specify the subject
    subject = "Welcome to Inkle!"
    
    # Specify the text body
    body_text = """Hi %s,

        Welcome to Inkle! Click on the following link to verify this email address and complete the registration process:

        http://www.inkleit.com/verifyEmail/%s/%s/

        Once your account is verified, you'll be able to log into Inkle and redefine how you plan your weekends!
    
    Welcome aboard,
    The Inkle team""" % (member.first_name, member.username, member.verification_hash)
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <p>Hi %s,</p>

            <p>Welcome to Inkle! Click <a href="http://www.inkleit.com/verifyEmail/%s/%s/">here</a> to verify your email address and start redefining how you plan your nights.</p>

            <p>Here are some suggestions to get you started:</p>
            
            <ol>
                <li><a href="http://www.inkleit.com/editProfile/information/">Update your profile information</a> to help your friends find you.</li>
                <li>Request to follow your friends by searching for them at the top of any page. If you're friends aren't using Inkle yet, use the link at the bottom of any page to tell them about it.</li>
                <li>Once your friends have accepted your request, <a href="http://www.inkleit.com/manage/blots/">group them into blots</a> (e.g. "Best Friends", "Dormmates", or "London Buddies").</li>
                <li>Join networks that you associate with by searching for them at the top of any page (e.g. "University of Notre Dame").</li>
                <li>See where people in your blots or networks are going or share where you will be headed by setting your own inklings from the <a href="http://www.inkleit.com/">home page</a>.
                <li>If you still have questions, check out the <a href="http://www.inkleit.com/help/">help section</a> or <a href="http://www.inkleit.com/contact/">contact us</a>.</li>
            </ol>
            
            <p>Welcome aboard,<br />
            The Inkle team</p>
        </body>
    </html>""" % (member.first_name, member.username, member.verification_hash)

    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)


def send_update_email_verification_email(member):
    """Sends update email verification email."""
    # Specify the from address and to addresses
    from_address = "inkle@inkleit.com"
    to_addresses = [member.email]

    # Specify the subject
    subject = "Confirm your new Inkle email address"
    
    # Specify the text body
    body_text = """Hi %s,

        Looks like you've changed the email address associated with your account. Click on the following link to verify this email address and get back to using Inkle:

        http://www.inkleit.com/verifyEmail/%s/%s/
    
    Welcome aboard,
    The Inkle team""" % (member.first_name, member.username, member.verification_hash)
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <p>Hi %s,</p>

            <p>Looks like you've changed the email address associated with your account. Click <a href="http://www.inkleit.com/verifyEmail/%s/%s/">here</a> to verify your new email address and get back to using <a href="http://www.inkleit.com">Inkle</a>.</p>
    
            <p>Welcome aboard,<br />
            The Inkle team</p>
        </body>
    </html>""" % (member.first_name, member.username, member.verification_hash)
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)


def send_password_reset_email(member):
    """Sends an email which allows member to reset their password."""
    # Specify the from address and to addresses
    from_address = "inkle@inkleit.com"
    to_addresses = [member.email]

    # Specify the subject
    subject = "Reset your Inkle password"
    
    # Specify the text body
    body_text = """Hi %s,

        We hear you forgot the password to your Inkle account! You can easily reset it using the link below. Note that you will only be able to visit this link one time. If you need another password reset link, go to the Inkle home page and request a new one.

        http://www.inkleit.com/resetPassword/%s/%s/

        If you didn't request to have your password reset, don't worry - just disregard this message.
    
    Thanks,
    The Inkle team""" % (member.first_name, member.username, member.verification_hash)
    
    # Specify the HTML body
    body_html = """<html>
        <head><head>
        <body>
            <p>Hi %s,</p>

            <p>You've requested to reset the password for your Inkle account. You can easily reset it by clicking <a href="http://www.inkleit.com/resetPassword/%s/%s/">here</a>. Note that you will only be able to visit this link one time. If you need another password reset link, go to the Inkle home page and request a new one.</p>

            <p>If you didn't request to have you password reset, don't worry - just disregard this message.</p>
    
            <p>Thanks,<br />
            The Inkle team</p>
        </body>
    </html>""" % (member.first_name, member.username, member.verification_hash)
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)


def send_request_to_follow_email(from_member, to_member):
    """Sends an email to to_member that from_member has requested to follow them."""
    # Specify the from address and to addresses
    from_address = "notifications@inkleit.com"
    to_addresses = [to_member.email]

    # Specify the subject
    subject = "%s %s has requested to follow you" % (from_member.first_name, from_member.last_name)
    
    # Determine whether to use his or her
    his_her = "his"
    if (from_member.gender == "Female"):
        his_her = "her"
    
    # Specify the text body
    body_text = """Hi %s,

        %s %s has requested to follow you on Inkle! Click on the following link to respond to %s request:

        http://www.inkleit.com/manage/requests/

    Thanks,
    The Inkle team""" % (to_member.first_name, from_member.first_name, from_member.last_name, his_her)
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <p>Hi %s,</p>

            <p>%s %s has requested to follow you on Inkle! Click <a href="http://www.inkleit.com/manage/notifications/">here</a> to respond to %s request.</p>
    
            <p>Thanks,<br />
            The Inkle team</p>
            
            <p style="font-size: 10px;">If you don't want to receive emails like this, you can set your email preferences <a href="http://www.inkleit.com/editProfile/emailPreferences/">here</a>.</p>
        </body>
    </html>""" % (to_member.first_name, from_member.first_name, from_member.last_name, his_her)
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)


def send_accept_request_email(from_member, to_member):
    """Sends an email to from_member that to_member has accepted their requested to follow them."""
    # Specify the from address and to addresses
    from_address = "notifications@inkleit.com"
    to_addresses = [from_member.email]

    # Determine whether to use his or her and him or her
    his_her = "his"
    him_her = "him"
    if (to_member.gender == "Female"):
        his_her = "her"
        him_her = "her"

    # Specify the subject
    subject = "%s %s has accepted your request to follow %s" % (to_member.first_name, to_member.last_name, him_her)
    
    # Specify the text body
    body_text = """Hi %s,

        %s %s has accepted your request to follow %s on Inkle! Click on the following link to check out %s profile:

        http://www.inkleit.com/member/%d/

    Thanks,
    The Inkle team""" % (from_member.first_name, to_member.first_name, to_member.last_name, him_her, his_her, to_member.id)
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <p>Hi %s,</p>

            <p>%s %s has accepted your request to follow %s on Inkle! Check out %s's inklings by visiting %s <a href="http://www.inkleit.com/member/%d/">profile</a> and group %s with the other people you are following by adding %s to your <a href="http://www.inkleit.com/manage/blots/">blots</a>.</p>
    
            <p>Thanks,<br />
            The Inkle team</p>
            
            <p style="font-size: 10px;">If you don't want to receive emails like this, you can set your email preferences <a href="http://www.inkleit.com/editProfile/emailPreferences/">here</a>.</p>
        </body>
    </html>""" % (from_member.first_name, to_member.first_name, to_member.last_name, him_her, to_member.first_name, his_her, to_member.id, him_her, him_her)
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)


def send_inkling_invitation_email(from_member, to_member, inkling):
    """Sends an email to from_member that to_member has invited them to the inkling."""
    # Specify the from address and to addresses
    from_address = "notifications@inkleit.com"
    to_addresses = [from_member.email]

    # Determine whether to use his or her and him or her
    his_her = "his"
    him_her = "him"
    if (from_member.gender == "Female"):
        his_her = "her"
        him_her = "her"

    # Determine the inkling category
    if (inkling.category == "dinner"):
        category = "Dinner"
    elif (inkling.category == "pregame"):
        category = "Pregame"
    elif (inkling.category == "mainEvent"):
        category = "Main Event"

    # Specify the subject
    subject = "%s %s has invited you to an inkling" % (from_member.first_name, from_member.last_name)
    
    # Specify the text body
    body_text = """Hi %s,

        %s %s has invited you to %s inkling! Here is the inkling's information:
        
        Location: %s
        Category: %s
        Date: %s

        You can respond to this inkling invitation by clicking on the following link:

        http://www.inkleit.com/manage/requests/

    Thanks,
    The Inkle team""" % (to_member.first_name, from_member.first_name, from_member.last_name, his_her, inkling.location.name, category, inkling.get_formatted_date())
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <p>Hi %s,</p>

            <p>%s %s has invited you to an inkling! Here is the information:</p>
            
            <p>Location: %s<br />
            Type: %s<br />
            Date: %s</p>

            <p>Click <a href="http://www.inkleit.com/manage/notifications/">here</a> to respond to %s invitation.</p>
    
            <p>Thanks,<br />
            The Inkle team</p>
            
            <p style="font-size: 10px;">If you don't want to receive emails like this, you can set your email preferences <a href="http://www.inkleit.com/editProfile/emailPreferences/">here</a>.</p>
        </body>
    </html>""" % (to_member.first_name, from_member.first_name, from_member.last_name, inkling.location.name, category, inkling.get_formatted_date(year = False, weekday = True), his_her)
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)


def send_contact_email(member, name, email, subject, message):
    """Sends a contact email to support@inkleit.com."""
    # Specify the from address and to addresses
    from_address = email
    to_addresses = ["support@inkleit.com"]

    # Specify the text body
    body_text = """Hi Jacob and Chad,
    
        Someone has sent a message using Inkle's contact page. Here is the information:

        Name: %s
        Message: %s
        Logged in: %s

    Thanks,
    The Inkle bot""" % (name, message, str(member != None))
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <p>Hi Jacob and Chad,</p>

            <p>Someone has sent a message using Inkle's contact page. Here is the information:</p>
            
            <p>Name: %s<br />
            Message: %s<br />
            Logged in: %s</p>

            <p>Thanks,<br />
            The Inkle bot</p>
        </body>
    </html>""" % (name, message, str(member != None))
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)


def send_invite_to_inkle_email(member, emails):
    """Sends an invitation to join Inkle to the inputted email."""
    # Specify the from address and to addresses
    from_address = "inkle@inkleit.com"
    to_addresses = emails

    # Specify the subject
    subject = "%s has invited you to join Inkle!" % (member.get_full_name())

    # Specify the text body
    body_text = """Hi there,
    
        %s has invited you to join Inkle! Inkle makes it easy to find where the big event is happening. To join, simply follow this link:

        http://www.inkleit.com/

        We hope to see you soon!

    Thanks,
    The Inkle team""" % (member.get_full_name())
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <p>%s has invited you to join Inkle!</p>

            <p>Inkle makes it easy to find where the big event is happening. Currently, Inkle is only available to Notre Dame, Saint Mary's, and Holy Cross students. To be one of the first members of the next big social network, click <a href="http://www.inkleit.com/">here</a>!</p>
            
            <p>Thanks,<br />
            The Inkle team</p>
        </body>
    </html>""" % (member.get_full_name())
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)
