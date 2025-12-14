from django import forms

class TitleSearch(forms.Form):
    search = forms.CharField(label='Wyszukaj po tytule', max_length=100)