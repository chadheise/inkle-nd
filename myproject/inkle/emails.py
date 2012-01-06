from smtplib import SMTP
from email.mime.text import MIMEText

live = False

def send_email(from_address, to_addresses, subject, body):
    """Sends an email with the inputted details using the WebFaction SMTP server."""
    # Create the message
    message = MIMEText(body)
    message["Subject"] = subject

    # Connect to the server, send the email, and disconnect from the server
    server = SMTP()
    server.connect("smtp.webfaction.com")
    server.login("inkle", "AmiTabh-2012")
    if (not live):
        to_addresses = ["jwenger@nd.edu", "cheise@nd.edu"]
    server.sendmail(from_address, to_addresses, message.as_string())
    server.quit()


def send_registration_email(member):
    """Sends the registration email."""
    from_address = "support@inkleit.com"
    to_addresses = [member.email]
    subject = "Welcome to Inkle!"
    body = """
        Hi %s,
           Welcome to Inkle! It'll lead you to a much better life.
        Peace,
        The Inkle team
    """ % (member.first_name)
    send_email(from_address, to_addresses, subject, body)
