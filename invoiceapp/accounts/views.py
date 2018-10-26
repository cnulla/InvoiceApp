from django.shortcuts import render, reverse
from django.contrib.auth import login, authenticate, logout
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from .models import MyUser, TokenGenerator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from accounts.forms import SignUpForm

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
            import pdb; pdb.set_trace()
            try:
                first_name = self.request.POST['first_name']
                last_name = self.request.POST['last_name']
                email = self.request.POST['email']
                user = form.save()
                token = user.generate_token()
                url = self.request.build_absolute_uri(reverse('verify_token', args=(token.token)))
                html_content = render_to_string('accounts/confirm_email.html', {'url': url, 'full_name': first_name+" "+last_name, 'email': email})
                subject, from_email, to = 'InvoiceApp Verification Email', settings.EMAIL_HOST_USER, [email]
                text_content = 'yes'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg = attach_alternative(html_content, 'text/html')
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
                user = MyUser.objects.get(email=token_obj.user)
                user.is_confirmed = True
                token_obj.is_used =True
                token_obj.save()
                TokenGenerator.objects.filter(user=user, is_used=False).delete()
                return render(self.request, self.template_name)
            return render(self.request, self.template_name, {'error_messages': 'Token has already expired.'})


class VerifyEmailView(TemplateView):
    """ Display instructions on verifying the email
    """
    template_name = 'accounts/verify_email.html'
