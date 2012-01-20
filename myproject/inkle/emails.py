from smtplib import SMTP_SSL
from email.mime.text import MIMEText

live = False

def send_email(from_address, to_addresses, subject, body_text, body_html):
    """Sends an email with the inputted details using the WebFaction SMTP server."""
    # Create the message
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
    from_address = "support@inkleit.com"
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
            <img src="http://www.inkleit.com/static/media/images/main/inkleLogo.png" />

            <p>Hi %s,</p>

            <p>Welcome to Inkle! Click <a href="http://www.inkleit.com/verifyEmail/%s/%s/">here</a> to verify this email address and complete the registration process.</p>

            <p>Once your account is verified, you'll be able to log into <a href="http://www.inkleit.com">Inkle</a> and redefine how you plan your weekends!</p>
    
            <p>Welcome aboard,<br />
            The Inkle team</p>
        </body>
    </html>""" % (member.first_name, member.username, member.verification_hash)

    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)


def send_update_email_verification_email(member):
    """Sends update email verification email."""
    # Specify the from address and to addresses
    from_address = "support@inkleit.com"
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
            <img src="http://www.inkleit.com/static/media/images/main/inkleLogo.png" />

            <p>Hi %s,</p>

            <p>Looks like you've changed the email address associated with your account. Click <a href="http://www.inkleit.com/verifyEmail/%s/%s/">here</a> to verify this email address and get back to using <a href="http://www.inkleit.com">Inkle</a>.</p>
    
            <p>Welcome aboard,<br />
            The Inkle team</p>
        </body>
    </html>""" % (member.first_name, member.username, member.verification_hash)
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)


def send_password_reset_email(member):
    """Sends an email which allows member to reset their password."""
    # Specify the from address and to addresses
    from_address = "support@inkleit.com"
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
            <img src="http://www.inkleit.com/static/media/images/main/inkleLogo.png" />

            <p>Hi %s,</p>

            <p>We hear you forgot the password to your Inkle account! You can easily reset it by clicking <a href="http://www.inkleit.com/resetPassword/%s/%s/">here</a>. Note that you will only be able to visit this link one time. If you need another password reset link, go to the Inkle home page and request a new one.</p>

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
    from_address = "support@inkleit.com"
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
            <img src="http://www.inkleit.com/static/media/images/main/inkleLogo.png" />

            <p>Hi %s,</p>

            <p>%s %s has requested to follow you on Inkle! Click <a href="http://www.inkleit.com/manage/requests/">here</a> to respond to %s request.</p>
    
            <p>Thanks,<br />
            The Inkle team</p>
        </body>
    </html>""" % (to_member.first_name, from_member.first_name, from_member.last_name, his_her)
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)


def send_accept_request_email(from_member, to_member):
    """Sends an email to from_member that to_member has accepted their requested to follow them."""
    # Specify the from address and to addresses
    from_address = "support@inkleit.com"
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

        %s %s has accpted your request to follow %s on Inkle! Click on the following link to check out %s profile:

        http://www.inkleit.com/member/%d/

    Thanks,
    The Inkle team""" % (from_member.first_name, to_member.first_name, to_member.last_name, him_her, his_her, to_member.id)
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <img src="http://www.inkleit.com/static/media/images/main/inkleLogo.png" />

            <p>Hi %s,</p>

            <p>%s %s has accpted your request to follow %s on Inkle! Click <a href="http://www.inkleit.com/member/%d/">here</a> to check out %s profile.</p>
    
            <p>Thanks,<br />
            The Inkle team</p>
        </body>
    </html>""" % (from_member.first_name, to_member.first_name, to_member.last_name, him_her, to_member.id, his_her)
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)
