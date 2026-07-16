from django import forms
from .models import Car,CarImage


class CarForm(forms.ModelForm):

    class Meta:

        model = Car

        exclude = (
            "owner",
            "approval_status",
            "is_available",
            "created_at",
            "updated_at",
        )

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Car Title"
            }),

            "brand": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Brand"
            }),

            "model": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Model"
            }),

            "year": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Year"
            }),

            "color": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Color"
            }),

            "seats": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Seats"
            }),

            "fuel_type": forms.Select(attrs={
                "class": "form-control"
            }),

            "transmission": forms.Select(attrs={
                "class": "form-control"
            }),

            "price_per_day": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Price Per Day"
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Describe your car..."
            }),

        }
    def clean_year(self):
        year = self.cleaned_data["year"]

        if year < 2010 or year > 2035:
            raise forms.ValidationError(
            "Please enter a valid manufacturing year."
        )

        return year


    def clean_price_per_day(self):
        price = self.cleaned_data["price_per_day"]

        if price <= 0:
            raise forms.ValidationError(
            "Price must be greater than zero."
        )

        return price


    def clean_seats(self):

        seats = self.cleaned_data["seats"]

        if seats < 2 or seats > 10:

            raise forms.ValidationError(
                "Seats must be between 2 and 10."
            )

        return seats




class CarImageForm(forms.ModelForm):

    class Meta:
        model = CarImage
        fields = ["image"]

        widgets = {
            "image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            )
        }