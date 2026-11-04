
import smtplib
import secrets
import os
import secrets
import smtplib

from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv


# Load .env from the project folder
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = os.getenv("SMTP_EMAIL")
SENDER_PASSWORD = os.getenv("SMTP_PASSWORD")

# Remove spaces from Gmail App Password
if SENDER_PASSWORD:
    SENDER_PASSWORD = SENDER_PASSWORD.replace(" ", "").strip()


# Generate six-digit OTP
def generate_otp():
    return str(secrets.randbelow(900000) + 100000)


# Send OTP email
def send_email(to_email, username, otp):

    try:
        # Check email credentials
        if not SENDER_EMAIL or not SENDER_PASSWORD:
            raise ValueError(
                "Email credentials are missing. Check your .env file."
            )

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

        # Connect to Gmail SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:

            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(SENDER_EMAIL, SENDER_PASSWORD)

            server.send_message(message)

        print("OTP email sent successfully.")
        return True

    except Exception as e:
        print("Error sending OTP email:", e)
        return False