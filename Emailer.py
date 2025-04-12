import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def mail_sender(reciever_email):
    # Sender and receiver details
    sender_email = "amsama1134@gmail.com"
    receiver_email = "ms.madhanyt@gmail.com"
    password = "gomiaayrucmfoorg"  # If 2FA is enabled, use an app password
    # Create the email content
    subject = "hey nigga" 
    body = "vishnu called"
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

mail_sender('watha')