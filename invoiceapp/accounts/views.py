from django.shortcuts import render, reverse
from django.contrib.auth import login, authenticate, logout
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect
from django.db import IntegrityError

from accounts.forms import SignUpForm

# Create your views here.

class SignUpView(TemplateView):
    template_name = 'accounts/signup.html'

    def get(self, *args, **kwargs):
        form = SignUpForm()
        return render(self.request, self.template_name, {'form': form})


    def post(self, *args, **kwargs):
        form = SignUpForm(self.request.POST)

        if form.is_valid():
            first_name = self.request.POST['first_name']
            last_name = self.request.POST['last_name']
            email = self.request.POST['email']
            form.save()
            print ('You are registered!')
        return render(self.request, self.template_name,{'form': form})
