from django.shortcuts import render, reverse, redirect
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect
from django.db import IntegrityError
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

from invoice.models import (
    Invitation,
    Client,
    Item,
    Invoice
    )

from .mixins import InvoiceMixins
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


class CreateInvoiceView(InvoiceMixins,TemplateView):
    """Create Invoice for client
    """
    template_name = 'invoiceapp/create_invoice.html'

    def get(self,*args, **kwargs):
        form = InvoiceForm()
        context = {
            'form': form,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = InvoiceForm(self.request.POST)
        if form.is_valid():
            invoice = form.save()
            items = self.request.POST.get('items')
            items = json.loads(items)
            for item in items:
                self.add_item(invoice, item)
            return HttpResponseRedirect(reverse('dashboard'))
        context = {
            'form': form,
        }
        return render(self.request, self.template_name, context)


class ItemFormView(TemplateView):
    """Item Form
    """
    template_name = 'invoiceapp/item_order_form.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'itm_form': ItemForm()})


class InvoiceView(TemplateView):
    """ Invoice Details
    """
    template_name = 'invoiceapp/invoice.html'

    def get(self, *args, **kwargs):
        item = Item.objects.all()
        return render(self.request, self.template_name, {'item':item})

