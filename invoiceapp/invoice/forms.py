from django import forms
from invoice.models import (
    Client,
    Company,
    Invitation,
    Item,
    Invoice,
    )

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
        model = Invitation
        fields = [
                'email'
        ]

        widgets = {
                'email': forms.TextInput(attrs={'class': 'form-control'})
        }


class DateInput(forms.DateInput):
    """ date picker
    """
    input_type = 'date'


class InvoiceForm(forms.ModelForm):
    """ Create invoice form
    """
    class Meta:
        model = Invoice
        fields = [
                'invoice_number', 'invoice_description', 'company', 'payment_status',
                'invoice_date', 'due_date', 'order_type', 'subtotal', 'less', 'total'
        ]

        widgets = {
                'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
                'invoice_description': forms.Textarea(attrs={'class': 'form-control'}),
                'company': forms.Select(attrs={'class': 'form-control'}),
                'payment_status': forms.CheckboxInput(attrs={'class': 'form-inline'}),
                'invoice_date': DateInput(),
                'due_date': DateInput(),
                'order_type': forms.Select(attrs={'class': 'form-control'}),
                'subtotal': forms.NumberInput(attrs={'class': 'form-control sub-total', 'readonly': 'readonly'}),
                'less': forms.NumberInput(attrs={'class': 'form-control less'}),
                'total': forms.NumberInput(attrs={'class': 'form-control invoice-total', 'readonly': 'readonly'})
        }


class ItemForm(forms.ModelForm):
    """ Create item form
    """
    class Meta:
        model = Item
        fields = [
            'order_number', 'order_description', 'order_date', 'end_date', 'amount',
            'item_type', 'rate', 'total_hours', 'total_amount', 'remarks'
        ]

        widgets = {
                'order_number': forms.NumberInput(attrs={'class': 'form-control'}),
                'order_description': forms.Textarea(attrs={'class': 'form-control'}),
                'order_date': DateInput(),
                'end_date': DateInput(),
                'amount': forms.NumberInput(attrs={'class': 'form-control amount'}),
                'item_type': forms.Select(attrs={'class': 'form-control item-type'}),
                'rate': forms.NumberInput(attrs={'class': 'form-control item-rate', 'disabled': 'disabled'}),
                'total_hours': forms.NumberInput(attrs={'class': 'form-control total-hours', 'disabled': 'disabled'}),
                'total_amount': forms.NumberInput(attrs={'class': 'form-control total-amount', 'disabled': 'disabled'}),
                'remarks': forms.Textarea(attrs={'class': 'form-control', 'required': False}),
        }
