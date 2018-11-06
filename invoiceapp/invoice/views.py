from django.shortcuts import render, reverse, redirect
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect

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
            invitation = form.save(commit=False)
            invitation.save()
            return HttpResponseRedirect(reverse('client'))
        return render(self.request, self.template_name, {'form': form })

