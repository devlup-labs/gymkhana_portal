from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'length': '10'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'length': '128'}))

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
