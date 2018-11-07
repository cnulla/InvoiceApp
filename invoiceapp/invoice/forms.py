from django import forms
from invoice.models import Client, Company


class ClientForm(forms.ModelForm):
    """ Creating forms for client
    """

    class Meta:
        model = Client
        fields = [
                'company', 'first_name', 'last_name', 'province', 'city', 'street', 'email'
                ]

        widgets = {
                'company': forms.Select(attrs={'class': 'form-control'}),
                'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Province'}),
                'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
                'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
                'email': forms.EmailInput(attrs={'class': 'form-control'}),

        }



    def clean_email(self):
        """Validate email
        """
        email = self.cleaned_data.get('email')
        email = email.lower()
        client = Client.objects.filter(email=email)

        if client.exists():
            raise forms.ValidationError('Email already exist')
        return email


class CompanyForm(forms.ModelForm):
    """ Creating forms for company
    """

    class Meta:
        model = Company
        fields = [
            'company_name'
        ]

        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class InvitationForm(forms.Form):
    """User send invitation form to the client
    """

    class Meta:
        model = Client
        fields = [
                'email'
        ]

        widgets = {
                'email': forms.TextInput(attrs={'class': 'form-control'})
        }
