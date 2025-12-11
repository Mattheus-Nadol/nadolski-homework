from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(label='Nazwa produktu', max_length=100)
    description = forms.CharField(label='Opis', widget=forms.Textarea)
    price = forms.DecimalField(label='Cena', max_digits=6, decimal_places=2)