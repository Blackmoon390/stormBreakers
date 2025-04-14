import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from numpy import rec


def mail_sender(reciever_email):
    # Sender and receiver details
    sender_email = "amsama1134@gmail.com"
    receiver_email = reciever_email
    password = "your google security token"  # If 2FA is enabled, use an app password
    # Create the email content
    subject = "consultation" 
    body = "patient called you for consultation \n ph:8866887765 \n address: 1234, 2nd cross, 3rd main, 4th block, 5th stage, 6th avenue, 7th street, 8th lane, 9th road, 10th area"
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

