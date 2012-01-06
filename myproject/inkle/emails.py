from smtplib import SMTP
from email.mime.text import MIMEText

live = False

def send_email(from_address, to_addresses, subject, body_text, body_html):
    """Sends an email with the inputted details using the WebFaction SMTP server."""
    # Create the message
    message = MIMEText(body_html, "html")
    message["Subject"] = subject

    # Connect to the server, send the email, and disconnect from the server
    server = SMTP()
    server.connect("smtp.webfaction.com")
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

        Welcome to Inkle! To complete the sign-up process, please verify this email address by clicking on the following link:

        http://www.inkleit.com/verifyEmail/%s/%s/

        Once you account is verified, you'll be able to log into Inkle and redefine how you plan your weekends!
    
    Welcome aboard,
    The Inkle team""" % (member.first_name, member.username, member.verification_hash)
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <img src="http://www.inkleit.com/static/media/images/main/inkleLogo.png" />

            <p>Hi %s,</p>

            <p>Welcome to Inkle! To complete the sign-up process, please verify this email address by clicking on the following link:</p>

            <a href="http://www.inkleit.com/verifyEmail/%s/%s/">http://www.inkleit.com/verifyEmail/%s/%s/</a>

            <p>Once you account is verified, you'll be able to log into <a href="http://www.inkleit.com">Inkle</a> and redefine how you plan your weekends!</p>
    
            <p>Welcome aboard,<br />
            The Inkle team</p>
        </body>
    </html>""" % (member.first_name, member.username, member.verification_hash, member.username, member.verification_hash)
    
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

        %s %s has requested to follow you on Inkle! To respond to %s request, head on over to Inkle:

        http://www.inkleit.com/manage/requests/

    Thanks,
    The Inkle team""" % (to_member.first_name, from_member.first_name, from_member.last_name, his_her)
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <img src="http://www.inkleit.com/static/media/images/main/inkleLogo.png" />

            <p>Hi %s,</p>

            <p>%s %s has requested to follow you on Inkle! To respond to %s request, head on over to <a href="http://www.inkleit.com/manage/requests/">Inkle</a>.</p>
    
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
    print "1"

    # Determine whether to use his or her and him or her
    his_her = "his"
    him_her = "him"
    if (to_member.gender == "Female"):
        his_her = "her"
        him_her = "her"
    print "2"

    # Specify the subject
    subject = "%s %s has accepted your request to follow %s" % (to_member.first_name, to_member.last_name, him_her)
    print "3"
    
    # Specify the text body
    body_text = """Hi %s,

        %s %s has accpted your request to follow %s on Inkle! To check out %s profile, head on over to Inkle:

        http://www.inkleit.com/member/%d/

    Thanks,
    The Inkle team""" % (from_member.first_name, to_member.first_name, to_member.last_name, him_her, his_her, to_member.id)
    print "4"
    
    # Specify the HTML body
    body_html = """<html>
        <head></head>
        <body>
            <img src="http://www.inkleit.com/static/media/images/main/inkleLogo.png" />

            <p>Hi %s,</p>

            <p>%s %s has accpted your request to follow %s on Inkle! To check out %s profile, head on over to <a href="http://www.inkleit.com/member/%d/">Inkle</a>.</p>
    
            <p>Thanks,<br />
            The Inkle team</p>
        </body>
    </html>""" % (from_member.first_name, to_member.first_name, to_member.last_name, him_her, his_her, to_member.id)
    print "5"
    
    # Send the email
    send_email(from_address, to_addresses, subject, body_text, body_html)
