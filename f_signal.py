import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv

load_dotenv()


def send_email(from_email: str, to_email: str, subject: str, mail_content: str) -> None:
    """
    Send an email via SendGrid: https://sendgrid.com/
    An API-key has to be obtained (free-plan is up to 100 emails per day)
    :param from_email: Verified email-address with SendGrid
    :param to_email: Email-address of the recepient
    :param subject: Subject of the email
    :param mail_content: Content of the email
    :return: 0
    """
    my_sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
    from_email_sg = Email(from_email)
    to_email_sg = To(to_email)
    subject_sg = subject
    content_sg = Content("text/plain", mail_content)
    mail = Mail(from_email_sg, to_email_sg, subject_sg, content_sg)
    mail_json = mail.get()
    # Send an HTTP POST request to /mail/send
    my_sg.client.mail.send.post(request_body=mail_json)
