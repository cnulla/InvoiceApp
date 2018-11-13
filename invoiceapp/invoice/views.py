from django.shortcuts import render, reverse, redirect
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from invoice.models import Invitation, Client
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core import mail
import json

from invoice.forms import (
    ClientForm,
    CompanyForm,
    InvoiceForm,
    ItemForm,
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


class CreateInvoiceView(TemplateView):
    """Create Invoice for client
    """
    template_name = 'invoiceapp/create_invoice.html'

    def get(self,*args, **kwargs):
        invoice_form = InvoiceForm()
        item_form = ItemForm()
        context = {
            'inv_form': invoice_form,
            'itm_form': item_form,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        import pdb; pdb.set_trace();
        invoice_form = InvoiceForm(self.request.POST)
        item_form = ItemForm(self.request.POST)
        success = False
        if invoice_form.is_valid():
            invoice = invoice_form.save(commit=False)
            invoice.save()
            success = True
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.save()
            success = True
        if success:
            return HttpResponseRedirect(reverse('dashboard'))
        context = {
            'inv_form': invoice_form,
            'itm_form': item_form
        }
        return render(self.request, self.template_name, context)


class ItemFormView(TemplateView):
    template_name = 'invoiceapp/item_order_form.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'itm_form': ItemForm()})
