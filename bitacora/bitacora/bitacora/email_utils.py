import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_mail_async(acceso, cleaned_data):
    def send_email():
        context = cleaned_data
        context['acceso_id'] = acceso.id
        html_message = render_to_string('emails/nuevo_acceso.html', {'data': context})

        subject = 'Nuevo acceso registrado'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['katalinagatita7520@gmail.com']

        email = EmailMessage(subject, html_message, from_email, recipient_list)
        email.content_subtype = 'html'
        email.send()

    thread = threading.Thread(target=send_email)
    thread.start()
