import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = "eshinhw@gmail.com"
EMAIL_PASSWORD = "qjsdfhgqdphqpbvd"

msg = EmailMessage()

msg['Subject'] = "Test 1"
msg['From'] = "eshinhw@gmail.com"
msg['To'] = "eshinhw@gmail.com"

msg.set_content(rebal.get_html_string())

# with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#     smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#     smtp.send_message(msg)
    
#     print('completed')