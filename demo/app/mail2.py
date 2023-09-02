
#To send an email with an attached image using Python, you can use the smtplib library for sending the email and the email.mime modules to construct the email message. Below is a step-by-step guide on how to send an email with an attached image:

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders



# Email configuration
sender_email = 'ranganathb.mca22@rvce.edu.in'
receiver_email = 'natarajveerapuradarsh@gmail.com'
subject = 'Image Attachment Test'
message = 'Here is your image attachment.'

# SMTP server configuration (for Gmail)
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Use 465 for SSL or 587 for TLS
smtp_username = 'ranganathb.mca22@rvce.edu.in'
smtp_password = 'Color2001smell'




# Create a MIMEMultipart object
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the text message
msg.attach(MIMEText(message, 'plain'))

# Attach the image
image_path = 'captured_image_1693632238.jpg'  # Replace with the actual path to your image
with open(image_path, 'rb') as image_file:
    image = MIMEImage(image_file.read(), name='image.jpg')
    msg.attach(image)
    
    
print("ashjsa")  
# Connect to the SMTP server
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Use this for TLS encryption
    server.login(smtp_username, smtp_password)  # Uncomment this line if you need to log in to your email account

    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email sent successfully")

except Exception as e:
    print(f"Error: {e}")

finally:
    print("ashjsa")
    server.quit()