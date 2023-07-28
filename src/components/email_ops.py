import smtplib
from bson import json_util
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email_with_json_attachment(sender_email, sender_password, receiver_email, json_data, filename="data.json"):
    try:
        # Convert the JSON data to a formatted string
        json_content = json_util.dumps(json_data)

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        # Add the current date and time to the subject
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subject = f"Recast update - {current_datetime}"
        msg['Subject'] = subject

        # Attach the JSON content as a file to the email
        attachment = MIMEApplication(json_content, _subtype="json")
        attachment.add_header('content-disposition', 'attachment', filename=filename)
        msg.attach(attachment)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.send_message(msg)

        print("Email with JSON attachment sent successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")

