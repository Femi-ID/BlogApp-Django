from django import forms
from .models import Comments
# form fields available, you can visit https://docs.djangoproject.com/en/3.0/ref/forms/fields/.


class EmailForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = {'name', 'email', 'body'}
        labels = {'name': "Enter name", 'mail': 'mail here!!'}
        widgets = {'body': forms.Textarea(attrs={'col': 50, 'row': 30})}


class SearchForm(forms.Form):
    query = forms.CharField()

