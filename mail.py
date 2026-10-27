import smtplib
import random

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Gmail SMTP settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# Your Gmail account
SENDER_EMAIL = "vanacharlalalithya@gmail.com"

# Gmail App Password
SENDER_PASSWORD = "zqrj kddg snsl wuxv"


# =========================================================
# GENERATE OTP
# =========================================================

def generate_otp():

    otp = str(random.randint(100000, 999999))

    return otp


# =========================================================
# SEND OTP EMAIL
# =========================================================

def send_email(to_email, username, otp):

    try:

        message = MIMEMultipart()

        message["From"] = SENDER_EMAIL
        message["To"] = to_email
        message["Subject"] = "Scholarship Portal - Password Reset OTP"

        body = f"""
Hello {username},

Your OTP for resetting your Scholarship Portal password is:

{otp}

This OTP is valid for 5 minutes.

Please do not share this OTP with anyone.

Regards,
Scholarship Portal Team
"""

        message.attach(
            MIMEText(body, "plain")
        )

        # Connect to Gmail SMTP
        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.starttls()

        # Login to Gmail
        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )

        # Send email
        server.sendmail(
            SENDER_EMAIL,
            to_email,
            message.as_string()
        )

        server.quit()

        print("OTP email sent successfully.")

        return True

    except Exception as e:

        print("Error sending OTP email:", e)

        return False