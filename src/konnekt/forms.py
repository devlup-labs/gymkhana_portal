from django import forms  # pragma: no use


class SkillSearchForm(forms.Form):  # pragma: no use
    search_text = forms.CharField(
        required=False,
        label='Search name or skill!',
        widget=forms.TextInput(attrs={'placeholder': 'Search name or skill...'})
    )
