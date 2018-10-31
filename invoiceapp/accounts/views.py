from django.shortcuts import render, reverse,redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from .models import MyUser, TokenGenerator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core import mail

from accounts.forms import SignUpForm, SignInForm

# Create your views here.

class SignUpView(TemplateView):
    """ User Sign Up/Registration
    """
    template_name = 'accounts/signup.html'

    def get(self, *args, **kwargs):
        form = SignUpForm()
        return render(self.request, self.template_name, {'form': form})


    def post(self, *args, **kwargs):
        form = SignUpForm(self.request.POST)
        if form.is_valid():
            try:
                first_name = self.request.POST['first_name']
                last_name = self.request.POST['last_name']
                email = self.request.POST['email']
                user = form.save()
                token = user.generate_token()
                url = self.request.build_absolute_uri(reverse('verify-token', args=(token.token,)))
                html_content = render_to_string('accounts/confirm_email.html', {'url': url, 'full_name': first_name+" "+last_name, 'email': email})
                subject, from_email, to = 'InvoiceApp Verification Email', settings.EMAIL_HOST_USER, [email]
                text_content = 'Verify Email'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
                return HttpResponseRedirect(reverse('verify-email'))
            except IntegrityError as e:
                context = {
                    'error_messages': 'Something went wrong. Please try again.'
                }
                return render(self.request, self.template_name, context)
        return render(self.request, self.template_name,{'form': form})



class VerifyTokenView(TemplateView):
        """ Verifying the token if existing or not
        """
        template_name = 'invoiceapp/dashboard.html'

        def get(self, *args, **kwargs):
            token = TokenGenerator.objects.filter(token=kwargs.get('token'), is_used=False)
            if token.exists():
                token_obj = token.first()
                user = MyUser.objects.get(email=token_obj.user.email)
                user.is_confirmed = True
                user.is_active = True
                token_obj.is_used =True
                user.save()
                token_obj.delete()
                return render(self.request, self.template_name)
            return render(self.request, self.template_name, {'error_messages': 'Token has already expired.'})


class VerifyEmailView(TemplateView):
    """ Display instructions on verifying the email
    """
    template_name = 'accounts/verify_email.html'


class SignInView(TemplateView):
    """ User Log In
    """
    template_name = 'accounts/signin.html'

    def get(self, *args, **kwargs):
        form = SignInForm()
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = SignInForm(self.request.POST)
        if form.is_valid():
            form.login_user(self.request)
            return render(self.request, 'invoiceapp/dashboard.html')
        return render(self.request, self.template_name, {'form': form})

