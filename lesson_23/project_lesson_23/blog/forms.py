from django import forms

class CommentSearch(forms.Form):
    min_comments = forms.IntegerField(
        label="Minimalna liczba komentarzy",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'np. 5', 'min': 0}),
        )


class ContactForm(forms.Form):
    name = forms.CharField(label="Imię", max_length=100)
    email = forms.EmailField(label="E-mail")
    message = forms.CharField(label="Wiadomość", widget=forms.Textarea)