from django.shortcuts import render, reverse, redirect
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from invoice.models import Invitation, Client
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core import mail

from invoice.forms import (
    ClientForm,
    CompanyForm,
    InvitationForm,
    )

# Create your views here.

class DashboardView(TemplateView):
    """ User Dashboard
    """
    template_name = 'invoiceapp/dashboard.html'


class ClientView(TemplateView):
    """ List of Clients
    """
    template_name = 'invoiceapp/clients.html'


class CreateClientView(TemplateView):
    """ Create a client
    """
    template_name = 'invoiceapp/create_clients.html'


    def get(self, *args, **kwargs):
        form = ClientForm()
        return render(self.request, self.template_name, {'form': form})


    def post(self, *args, **kwargs):
        form = ClientForm(self.request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return HttpResponseRedirect(reverse('client'))
        return render(self.request, self.template_name, {'form': form})


class CreateCompanyView(TemplateView):
    """ Create company
    """
    template_name = 'invoiceapp/create_company.html'


    def get(self, *args, **kwargs):
        form = CompanyForm()
        return render(self.request, self.template_name, {'form': form})


    def post(self, *args, **kwargs):
        form = CompanyForm(self.request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            return HttpResponseRedirect(reverse('client'))
        return render(self.request, self.template_name, {'form': form})


class InvitationView(TemplateView):
    """ User send invitation to client
    """
    template_name = 'invoiceapp/invitation.html'


    def get(self, *args, **kwargs):
        form = InvitationForm()
        return render(self.request, self.template_name, {'form': form})


    def post(self, *args, **kwargs):
        form = InvitationForm(self.request.POST)
        if form.is_valid():
            try:
                import pdb; pdb.set_trace()
                invitation = form.save(commit=False)
                email = self.request.POST['email']
                invitation.client = self.request.user
                invitation.email = email
                invitation.save()
                token = invitation.generate_token()
                url = self.request.build_absolute_uri(reverse('verify-invitation', args=(token.token,)))
                html_content = render_to_string('invoice/accept_invite.html', {'url': url, 'email': email})
                subject, from_email, to = 'InvoiceApp Invitation Email', settings.EMAIL_HOST_USER, [email]
                msg = EmailMultiAlternatives(subject, from_email, [to])
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
                return HttpResponseRedirect(reverse('client'))
            except IntegrityError as e:
                context = {
                    'error_messages': 'Something went wrong. Please try again.'
                }
                return render(self.request, self.template_name, context)
        return render(self.request, self.template_name,{'form': form})


class VerifyInvitationView(View):
    """Verifying the invitation/token if existing or not
    """

    def get(self, *args, **kwargs):
            token = Invitation.objects.filter(token=kwargs.get('token'), is_used=False)
            if token.exists():
                token_obj = token.first()
                token_obj.is_used = True
                token_obj.delete()
                return HttpResponseRedirect(reverse('client'))
            return render(self.request, 'invoice/clients.html', {'error_messages': 'Token has already expired.'})


