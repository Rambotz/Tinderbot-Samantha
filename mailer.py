import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()
# Define the email sender and recipient

def email_sender(email):

    sender = os.getenv('EMAIL')
    recipient = os.getenv('EMAILRECIVIER')

    # Create a MIME message object
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = os.getenv('MAILSUBJECT')

    # Add some text to the message
    body = os.getenv('MAILMESSAGE')
    message.attach(MIMEText(body, "plain"))

    # Define the SMTP server and port
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Connect to the SMTP server and authenticate
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(sender, os.getenv('PASSWORD'))

    # Send the email
    smtp_connection.sendmail(sender, recipient, message.as_string())

    # Disconnect from the SMTP server
    smtp_connection.quit()
