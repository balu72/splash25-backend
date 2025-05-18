import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, render_template

def send_invitation_email(invited_buyer):
    """Send invitation email to buyer"""
    sender_email = current_app.config.get('MAIL_USERNAME', 'noreply@splash25.com')
    receiver_email = invited_buyer.email
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Invitation to Register for Splash25"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Create the plain-text and HTML version of your message
    text = f"""
    Hello {invited_buyer.name},
    
    You have been invited to register for Splash25, the premier travel event in Wayanad.
    
    Please click the link below to complete your registration:
    {current_app.config.get('FRONTEND_URL', 'http://localhost:5173')}/register/{invited_buyer.invitation_token}
    
    This invitation is valid for 7 days.
    
    Best regards,
    The Splash25 Team
    """
    
    html = f"""
    <html>
      <body>
        <p>Hello {invited_buyer.name},</p>
        <p>You have been invited to register for <strong>Splash25</strong>, the premier travel event in Wayanad.</p>
        <p>Please click the button below to complete your registration:</p>
        <p>
          <a href="{current_app.config.get('FRONTEND_URL', 'http://localhost:5173')}/register/{invited_buyer.invitation_token}" 
             style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">
            Complete Registration
          </a>
        </p>
        <p>This invitation is valid for 7 days.</p>
        <p>Best regards,<br>The Splash25 Team</p>
      </body>
    </html>
    """
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part1)
    message.attach(part2)
    
    # Send email
    try:
        # Check if email is configured
        if not current_app.config.get('MAIL_SERVER') or not current_app.config.get('MAIL_PORT'):
            current_app.logger.warning("Email service not configured. Skipping email send.")
            return False
            
        server = smtplib.SMTP_SSL(
            current_app.config.get('MAIL_SERVER'), 
            current_app.config.get('MAIL_PORT')
        )
        server.login(
            current_app.config.get('MAIL_USERNAME'), 
            current_app.config.get('MAIL_PASSWORD')
        )
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False

def send_registration_confirmation_email(pending_buyer):
    """Send confirmation email after registration"""
    sender_email = current_app.config.get('MAIL_USERNAME', 'noreply@splash25.com')
    receiver_email = pending_buyer.email
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Registration Received for Splash25"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Create the plain-text and HTML version of your message
    text = f"""
    Hello {pending_buyer.name},
    
    Thank you for registering for Splash25!
    
    Your registration has been received and is currently under review. We will notify you once it has been approved.
    
    Best regards,
    The Splash25 Team
    """
    
    html = f"""
    <html>
      <body>
        <p>Hello {pending_buyer.name},</p>
        <p>Thank you for registering for <strong>Splash25</strong>!</p>
        <p>Your registration has been received and is currently under review. We will notify you once it has been approved.</p>
        <p>Best regards,<br>The Splash25 Team</p>
      </body>
    </html>
    """
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part1)
    message.attach(part2)
    
    # Send email
    try:
        # Check if email is configured
        if not current_app.config.get('MAIL_SERVER') or not current_app.config.get('MAIL_PORT'):
            current_app.logger.warning("Email service not configured. Skipping email send.")
            return False
            
        server = smtplib.SMTP_SSL(
            current_app.config.get('MAIL_SERVER'), 
            current_app.config.get('MAIL_PORT')
        )
        server.login(
            current_app.config.get('MAIL_USERNAME'), 
            current_app.config.get('MAIL_PASSWORD')
        )
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False

def send_approval_email(user, password):
    """Send approval email with login credentials"""
    sender_email = current_app.config.get('MAIL_USERNAME', 'noreply@splash25.com')
    receiver_email = user.email
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Splash25 Registration Has Been Approved"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Create the plain-text and HTML version of your message
    text = f"""
    Hello {user.username},
    
    Your registration for Splash25 has been approved!
    
    You can now log in to your account using the following credentials:
    
    Username: {user.username}
    Password: {password}
    
    Please change your password after your first login.
    
    Best regards,
    The Splash25 Team
    """
    
    html = f"""
    <html>
      <body>
        <p>Hello {user.username},</p>
        <p>Your registration for <strong>Splash25</strong> has been approved!</p>
        <p>You can now log in to your account using the following credentials:</p>
        <p>
          <strong>Username:</strong> {user.username}<br>
          <strong>Password:</strong> {password}
        </p>
        <p>Please change your password after your first login.</p>
        <p>
          <a href="{current_app.config.get('FRONTEND_URL', 'http://localhost:5173')}/login" 
             style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">
            Login to Your Account
          </a>
        </p>
        <p>Best regards,<br>The Splash25 Team</p>
      </body>
    </html>
    """
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part1)
    message.attach(part2)
    
    # Send email
    try:
        # Check if email is configured
        if not current_app.config.get('MAIL_SERVER') or not current_app.config.get('MAIL_PORT'):
            current_app.logger.warning("Email service not configured. Skipping email send.")
            return False
            
        server = smtplib.SMTP_SSL(
            current_app.config.get('MAIL_SERVER'), 
            current_app.config.get('MAIL_PORT')
        )
        server.login(
            current_app.config.get('MAIL_USERNAME'), 
            current_app.config.get('MAIL_PASSWORD')
        )
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False

def send_rejection_email(pending_buyer):
    """Send rejection email"""
    sender_email = current_app.config.get('MAIL_USERNAME', 'noreply@splash25.com')
    receiver_email = pending_buyer.email
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Regarding Your Splash25 Registration"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Create the plain-text and HTML version of your message
    text = f"""
    Hello {pending_buyer.name},
    
    Thank you for your interest in Splash25.
    
    We regret to inform you that your registration could not be approved at this time.
    
    If you have any questions, please contact our support team.
    
    Best regards,
    The Splash25 Team
    """
    
    html = f"""
    <html>
      <body>
        <p>Hello {pending_buyer.name},</p>
        <p>Thank you for your interest in <strong>Splash25</strong>.</p>
        <p>We regret to inform you that your registration could not be approved at this time.</p>
        <p>If you have any questions, please contact our support team.</p>
        <p>Best regards,<br>The Splash25 Team</p>
      </body>
    </html>
    """
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part1)
    message.attach(part2)
    
    # Send email
    try:
        # Check if email is configured
        if not current_app.config.get('MAIL_SERVER') or not current_app.config.get('MAIL_PORT'):
            current_app.logger.warning("Email service not configured. Skipping email send.")
            return False
            
        server = smtplib.SMTP_SSL(
            current_app.config.get('MAIL_SERVER'), 
            current_app.config.get('MAIL_PORT')
        )
        server.login(
            current_app.config.get('MAIL_USERNAME'), 
            current_app.config.get('MAIL_PASSWORD')
        )
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False
