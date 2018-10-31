from django.shortcuts import render, reverse, redirect
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect

# Create your views here.

class DashboardView(TemplateView):
    template_name = 'invoiceapp/dashboard.html'

