from typing import Dict, List

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


User = get_user_model()


def send_html_to_email(
    to_list: List,
    subject: str,
    template_name,
    context: Dict,
    sender=settings.DEFAULT_FROM_EMAIL,
):
    # Parse html to string
    email_html_message = render_to_string(template_name, context)
    # Initialize a single email message which can be send to multiple recipients
    msg = EmailMultiAlternatives(
        subject=subject, body=email_html_message, from_email=sender, to=to_list
    )
    # Changes content type to text/html
    msg.content_subtype = "html"
    # Sends email and fail silently
    return msg.send()
