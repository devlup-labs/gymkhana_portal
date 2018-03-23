from django import forms


class SkillSearchForm(forms.Form):
    search_text = forms.CharField(
        required=False,
        label='Search name or skill!',
        widget=forms.TextInput(attrs={'placeholder': 'Search name or skill...'})
    )