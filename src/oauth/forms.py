from datetime import date, timedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from .models import UserProfile, SocialLink


class UserProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'length': '10'}))
    about = forms.TextInput(attrs={'class': 'md-textarea', 'length': '160'})
    year = forms.ChoiceField(choices=UserProfile.YEAR_CHOICES, widget=forms.Select(attrs={'class': 'mdb-select'}))

    class Meta:
        model = UserProfile
        fields = ['year', 'phone', 'avatar', 'cover', 'hometown', 'skills', 'about']


class SocialLinkForm(forms.ModelForm):

    class Meta:
        model = SocialLink
        fields = ['social_media', 'link']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        links = SocialLink.objects.filter(user=user)
        taken_choices = []
        for link in links:
            for key, value in SocialLink.SM_CHOICES:
                if link.social_media == key:
                    taken_choices += [(key, value)]
        super(SocialLinkForm, self).__init__(*args, **kwargs)
        self.fields['social_media'].choices = sorted(set(self.fields['social_media'].choices) ^ set(taken_choices))


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'maxlength': '254'}))
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Password confirmation',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Enter the same password as before, for verification.',
    )
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, widget=forms.Select(attrs={'class': 'mdb-select'}))
    roll = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(label='Date of birth',
                          widget=forms.TextInput(
                              attrs={'class': 'form-control datepicker', 'placeholder': 'Pick a date'}))
    prog = forms.ChoiceField(choices=UserProfile.PROG_CHOICES, widget=forms.Select(attrs={'class': 'mdb-select'}))
    year = forms.ChoiceField(choices=UserProfile.YEAR_CHOICES, widget=forms.Select(attrs={'class': 'mdb-select'}))
    phone = forms.CharField(max_length=10, validators=[UserProfile.contact],
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    branch = forms.ChoiceField(choices=UserProfile.BRANCH_CHOICES, widget=forms.Select(attrs={'class': 'mdb-select'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

    def clean_email(self):
        if not self.data['email'].endswith('@iitj.ac.in'):
            raise forms.ValidationError('Not a valid email address')
        elif User.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('Email address is already registered')
        else:
            return self.data['email'].lower()

    def clean_username(self):
        username_submit = self.data['username']
        e_username = self.data['email'].split('@')[0]
        if username_submit != e_username:
            raise forms.ValidationError("Username doesn't comply with provided email")
        else:
            return self.data['username'].lower()

    def clean_roll(self):
        if len(self.data['roll']) < 7:
            raise forms.ValidationError('Not a valid enrollment number')
        if UserProfile.objects.filter(roll__iexact=self.data['roll'].upper()).exists():
            raise forms.ValidationError('This enrollment number is already in use')
        else:
            return self.data['roll'].upper()

    def clean_dob(self):
        dob_date = self.cleaned_data['dob']
        if dob_date > date.today() - timedelta(days=13 * 365):
            raise forms.ValidationError("You must be greater than 13 years")
        return self.cleaned_data['dob']
