#ranganatth80@gmail.com
#natarajveerapuradarsh@gmail.com
#ssiucbexhojqysgy

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

server.login('ranganathb.mca22@rvce.edu.in','Color2001smell')

msg = MIMEMultipart()
msg['Subject'] = 'Image Attachment Test'

    # Add text to the email
body = 'This is a test email with an image attachment.'
msg.attach(MIMEText(body, 'plain'))


    # Attach an image to the email
image_path = 'captured_image_1693632238.jpg'    
with open(image_path, 'rb') as image_file:
    image = MIMEImage(image_file.read(), name='image.jpg')
    msg.attach(image)
#print(msg.as_string())
try:
    # ... your code ...
    server.sendmail('ranganathb.mca22@rvce.edu.in', 'natarajveerapuradarsh@gmail.com', msg.as_string())
    print("Email sent successfully")
except Exception as e:
    print(f"Error: {e}")
print("A")
print("babas")
#server = smtplib.SMTP('smtp.gmail.com',587)
#server.starttls()
#server.login('ranganathb.mca22@rvce.edu.in','Color2001smell')
#server.sendmail('ranganathb.mca22@rvce.edu.in','natarajveerapuradarsh@gmail.com','hey')
#print("asas")
#image_path = 'captured_image_1693632238.jpg'
#print("asas")
#send_email(image_path)
