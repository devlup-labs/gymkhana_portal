from django import forms
from .models import Topic, Answer
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.html import strip_tags


class TopicForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Topic
        fields = ['category', 'title', 'tags', 'content']


class AnswerForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Answer
        fields = ('topic', 'author', 'content')

    def clean_content(self):
        content = strip_tags(self.data['content']).split()
        content = [x for x in content if x != '&nbsp;']
        if len(content) == 0:
            raise forms.ValidationError('This field is required')
        else:
            return self.data['content']
