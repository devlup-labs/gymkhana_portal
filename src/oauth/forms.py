from datetime import date, timedelta
from django import forms
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


class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, widget=forms.Select(attrs={'class': 'mdb-select'}))
    roll = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(label='Date of Birth',
                          widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control select-wrapper'}))
    prog = forms.ChoiceField(choices=UserProfile.PROG_CHOICES, widget=forms.Select(attrs={'class': 'mdb-select'}))
    year = forms.ChoiceField(choices=UserProfile.YEAR_CHOICES, widget=forms.Select(attrs={'class': 'mdb-select'}))
    phone = forms.CharField(max_length=10, validators=[UserProfile.contact],
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    branch = forms.ChoiceField(choices=UserProfile.BRANCH_CHOICES, widget=forms.Select(attrs={'class': 'mdb-select'}))

    class Meta:
        model = UserProfile
        fields = ['gender', 'roll', 'dob', 'prog', 'year', 'phone', 'branch']

    def clean_dob(self):
        dob_date = self.cleaned_data['dob']
        if dob_date > date.today() - timedelta(days=13 * 365):
            raise forms.ValidationError("You must be greater than 13 years")
        return self.cleaned_data['dob']
