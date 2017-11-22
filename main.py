import config
import datetime
import smtplib
from database import *

# SMTP settings
sender = config.GMAIL_USERNAME
username = config.GMAIL_USERNAME
password = config.GMAIL_PASSWORD

# Connect to database
db.connect()

# Get admin's 'save photo' property
admin = Users.select().where(Users.admin == True)
save_photo = admin[0].save_photo

# Create array of receivers
query = Users.select().where(Users.send_notification == True)
receivers = []
for user in query:
    receivers.append(user.email)

# Close db connection
db.close()

# If someone was detected
# Direction of the event take from analyzed video
walked_in = True # False

# Date of the event
date = datetime.datetime.now()

if save_photo:
    # Photo name of the event
    date_converted = date.strftime('%d%m%Y%H%M%S')
    photo_name = 'photo_' + date_converted + '.jpeg'

    # Save photo
    path = config.PHOTO_PATH + photo_name
    # save
else:
  photo_name = 'no photo'

# Save event in database
db.connect()
Events.create(walked_in=walked_in, created_at=date, updated_at=date, photo=photo_name)
db.close()

# Send email to every who wants notifications
if any(receivers):
    # Prepare email's message
    direction = 'in' if walked_in else 'out'

    msg = """From: %s
    Subject: Someone just walked %s!

    Date of the event: %s.
    """ % (sender, direction, date.strftime('%d %b %Y %H:%M:%S'))

    if save_photo: msg += "Photo was taken."

    # Send email to receivers
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(sender, receivers, msg)
    server.quit()
