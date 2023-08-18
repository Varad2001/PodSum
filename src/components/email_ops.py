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


        # get the data
        """
        new_episodes = json_data['new_episodes']
        message = "<html><body>"
        for new_episode in new_episodes:
            new_data = f\"""
            Title : {new_episode['episode_title']} \n
            URL : {new_episode['episode_url']} \n
            Podcast : {new_episode['podcast_name']} \n
            Summary : {new_episode['summary']}
            \"""
            message = message + "\n\n" + new_data
        """
        message = parse_data(json_data=json_data)
        msg.attach(MIMEText(message, 'html'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.send_message(msg)

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")


def parse_data(json_data):
    # Create an HTML template for the email content
    html_template = """
    <html>
    <head>
    <style>
        /* Add your CSS styling here */
        body {
            font-family: Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
        }
        .episode {
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 20px;
            background-color: #f9f9f9;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            text-decoration: none;
        }
        .title:hover {
            text-decoration: underline;
        }
        .podcast {
            font-size: 18px;
            margin-top: 10px;
            color: #666;
        }
        .summary {
            margin-top: 10px;
            color: #444;
        }
    </style>
    </head>
    <body>
        <h1 style="font-size: 28px;">Latest Podcast Episodes</h1>
        %s
    </body>
    </html>
    """
    # Generate HTML content by iterating through episodes
    episode_html = ""
    episodes = json_data['new_episodes']
    for episode in episodes:
        episode_html += """
        <div class="episode">
            <a href="{episode_url}" class="title">{episode_title}</a>
            <p><strong>Podcast:</strong> {podcast_name}</p>
            <p class="summary">{summary}</p>
        </div>
        """.format(**episode)

    # Fill the template with the generated episode HTML
    html_content = html_template % episode_html

    return html_content



if __name__ == "__main__":
    data = {"new_episodes": [
        {"episode_url": "https://www.youtube.com/watch?v=QDOk-RAHexg", "episode_title": "Legendary 85-Year-Old Physical Therapist Dr. Shirley Sahrmann Reveals Her Exercise Routine", "podcast_name": "timferriss", "summary": " The speaker, a PhD in neurobiology, shares their journey of learning about musculoskeletal issues, nutrition, and physical activity. They have a few funny stories along the way, such as realizing that their pants were backwards from doing a quadruped exercise, and needing to change their finger grips for bowling due to their hand movements. They discuss the importance of understanding femoral retroversion for activities such as deadlifts and golf, as well as the importance of physical therapy in understanding the connection between the backbone, pelvic bone, knee, and hip."},
        {"episode_url": "https://www.youtube.com/watch?v=KPhd-Qua72E", "episode_title": "Legendary 85-Year-Old Physical Therapist Dr. Shirley Sahrmann Reveals Her Exercise Routine", "podcast_name": "timferriss", "summary": " The speaker, a PhD in neurobiology, shares their journey of learning about musculoskeletal issues, nutrition, and physical activity. They have a few funny stories along the way, such as realizing that their pants were backwards from doing a quadruped exercise, and needing to change their finger grips for bowling due to their hand movements. They discuss the importance of understanding femoral retroversion for activities such as deadlifts and golf, as well as the importance of physical therapy in understanding the connection between the backbone, pelvic bone, knee, and hip."}
        
        ]
        }
    
    send_email_with_json_attachment(
        sender_email= "testingrecast@gmail.com",
        sender_password="vkcwuujfemmpmvdu",
        receiver_email="vktesting4@gmail.com",
        json_data=data
    )


