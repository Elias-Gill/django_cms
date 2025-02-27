from django import forms

from modulos.Categories.models import Category


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "status", "moderacion", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "moderacion": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
