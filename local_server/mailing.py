
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from config import settings


def send_email(sub: str, message: str, sender_address: str, receiver_address: str, receiver_full_name: str, sender_full_name: str) -> bool:
    subject = f"Message from Diabetes App | {sub} |"
    body = f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f6f6f6;">
        <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <!-- Header -->
            <div style="background-color: #2196F3; padding: 30px; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">Diabetes App</h1>
                <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0; font-size: 14px;">Your Health Companion</p>
            </div>

            <!-- Content -->
            <div style="padding: 30px;">
                <p style="font-size: 16px; color: #333; margin: 0 0 20px;">Dear {receiver_full_name},</p>
                
                <!-- Message Card -->
                <div style="background: #f8f9fa; border-left: 4px solid #2196F3; padding: 20px; margin: 20px 0; border-radius: 4px;">
                    {message}
                </div>

                <!-- Footer -->
                <div style="border-top: 1px solid #eee; padding-top: 20px; margin-top: 30px;">
                    <p style="margin: 0 0 10px; color: #666;">Best Regards,</p>
                    <p style="margin: 0; font-weight: 600; color: #333;">{sender_full_name}</p>
                    <p style="margin: 5px 0 0; color: #666; font-size: 14px;">{sender_address}</p>
                </div>
            </div>

            <!-- Copyright -->
            <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 0 0 10px 10px;">
                <p style="margin: 0; color: #999; font-size: 12px;">
                    This email was sent from the Diabetes App notification system. 
                    Please do not reply directly to this message.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = receiver_address
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(body, 'html'))

    # SMTP configuration
    smtp_server = settings.SMTP_SERVER
    port = 587
    smtp_user = settings.SMTP_USER
    smtp_password = settings.SMTP_PASSWORD

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()
    return True

