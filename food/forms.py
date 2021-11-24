from django import forms
from .models import Category


class ItemCreationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Name'})
        self.fields['price'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Price'})
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Category'})
        self.fields['category'].queryset = Category.objects.filter(user=user)

    name = forms.CharField()
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    category = forms.ModelChoiceField(queryset=None)
    image = forms.ImageField()


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
