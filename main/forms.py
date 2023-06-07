from django import forms
from .models import Categories, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CategoryFilterForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'required':False})
    )

    class Meta:
        model = Categories
        fields = {'categories'}

    def __init__(self, *args, **kwargs):
        super(CategoryFilterForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = Categories.objects.all()