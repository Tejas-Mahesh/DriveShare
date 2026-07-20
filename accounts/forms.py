from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)

    email = forms.EmailField()

    phone_number = forms.CharField(max_length=15)

    class Meta:

        model = CustomUser

        fields = (

            'user_type',

            'username',

            'first_name',

            'email',

            'phone_number',

            'password1',

            'password2',

        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user_type"].choices = [
            ("customer", "Customer"),
            ("owner", "Car Owner"),
        ]
from django import forms
from .models import CustomerProfile, OwnerProfile


class CustomerProfileForm(forms.ModelForm):

    class Meta:

        model = CustomerProfile

        fields = [
            "address",
            "date_of_birth",
            "aadhaar_number",
            "aadhaar_photo",
            "driving_license_number",
            "driving_license_photo",
            "emergency_contact",
        ]

        widgets = {

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "aadhaar_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter 12-digit Aadhaar Number"
                }
            ),

            "driving_license_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "emergency_contact": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }

    def clean_aadhaar_number(self):

        aadhaar = self.cleaned_data["aadhaar_number"]

        if len(aadhaar) != 12 or not aadhaar.isdigit():

            raise forms.ValidationError(
                "Aadhaar number must contain exactly 12 digits."
            )

        return aadhaar


class OwnerProfileForm(forms.ModelForm):

    class Meta:

        model = OwnerProfile

        fields = [
            "address",
            "aadhaar_number",
            "aadhaar_photo",
            "driving_license_number",
            "driving_license_photo",
            "pan_number",
            "bank_account",
            "ifsc_code",
        ]

        widgets = {

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "aadhaar_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "driving_license_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "pan_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "bank_account": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "ifsc_code": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }

    def clean_aadhaar_number(self):

        aadhaar = self.cleaned_data["aadhaar_number"]

        if len(aadhaar) != 12 or not aadhaar.isdigit():

            raise forms.ValidationError(
                "Aadhaar number must contain exactly 12 digits."
            )

        return aadhaar

    def clean_pan_number(self):

        pan = self.cleaned_data["pan_number"]

        if len(pan) != 10:

            raise forms.ValidationError(
                "PAN number must contain 10 characters."
            )

        return pan.upper()

    def clean_ifsc_code(self):

        ifsc = self.cleaned_data["ifsc_code"]

        if len(ifsc) != 11:

            raise forms.ValidationError(
                "IFSC Code must contain 11 characters."
            )

        return ifsc.upper()
from .models import CustomUser


class ProfilePictureForm(forms.ModelForm):

    class Meta:

        model = CustomUser

        fields = [
            "profile_picture",
        ]

        widgets = {

            "profile_picture": forms.FileInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }