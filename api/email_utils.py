import resend
from decouple import config
from django.template.loader import render_to_string

resend.api_key = config("RESEND_API_KEY")

def send_resend_email(to, subject, template_name, context, from_email="noreply@yourdomain.com"):
    """
    Renders a Django template and sends it as an email using RESEND.
    """
    html = render_to_string(template_name, context)
    return resend.Emails.send({
        "from": from_email,
        "to": to,
        "subject": subject,
        "html": html
    })

