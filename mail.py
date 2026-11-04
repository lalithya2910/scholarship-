
import smtplib
import secrets
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = os.getenv("SMTP_EMAIL")
SENDER_PASSWORD = os.getenv("SMTP_PASSWORD")


# Generate six-digit OTP
def generate_otp():
    return str(secrets.randbelow(900000) + 100000)


# Send OTP email
def send_email(to_email, username, otp):

    try:
        if not SENDER_EMAIL or not SENDER_PASSWORD:
            raise ValueError("Email credentials are missing.")

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

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)

        print("OTP email sent successfully.")
        return True

    except Exception as e:
        print("Error sending OTP email:", e)
        return False
