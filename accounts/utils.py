from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings

def detect_user(user):
    if user.role == 1:
        redirect_url = reverse('clinicDashboard')  # Assuming you have a named URL pattern for clinicDashboard
    elif user.role == 2:
        redirect_url = reverse('customerDashboard')  # Assuming you have a named URL pattern for customerDashboard
    elif user.role is None and user.is_superadmin:
        redirect_url = '/admin'
    return redirect_url

def send_verification_email(request, user,subject, template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    subject = subject
    message = render_to_string(template, {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(subject, message, from_email, to=[to_email])
    mail.send()
    
# def send_reset_password_email(request,user):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     current_site = get_current_site(request)
#     subject = 'Reset your password'
#     message = render_to_string('reset_password_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': default_token_generator.make_token(user),
#     })
#     to_email = user.email
#     mail = EmailMessage(subject, message, from_email, to=[to_email])
#     mail.send()

def send_notification(subject,template,context):
    from_email = settings.DEFAULT_FROM_EMAIL
    mail = EmailMessage(subject, render_to_string(template, context), from_email, to=[context['user'].email])
    mail.send()