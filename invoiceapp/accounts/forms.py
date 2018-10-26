from django import forms
from accounts.models import MyUser
from django.contrib.auth import authenticate


class SignUpForm(forms.ModelForm):

    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'minLength': 8, 'placeholder': 'Password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'minLength': 8, 'placeholder': 'Confirm Password'}), required=True)

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password doesn/t match.')
        return confirm_password


    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        user = MyUser.objects.filter(email=email)
        if user.exists():
            raise form.ValidationError('Email is already taken.')
        return email


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user




