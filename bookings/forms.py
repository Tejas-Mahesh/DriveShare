from django import forms
from .models import Booking
from .models import Booking, Review

class BookingForm(forms.ModelForm):
    coupon_code = forms.CharField(

    required=False,

    max_length=30,

    widget=forms.TextInput(

        attrs={

            "placeholder":"Enter Coupon Code"

        }

    )

)

    class Meta:

        model = Booking

        fields = (
            "start_date",
            "end_date",
            "customer_message",
        )

        widgets = {

            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "customer_message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Any special requests for the owner..."
                }
            ),
        }

from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = [
            "rating",
            "review"
        ]

        widgets = {

            "rating": forms.Select(

                choices=[
                    (1,"⭐ 1"),
                    (2,"⭐⭐ 2"),
                    (3,"⭐⭐⭐ 3"),
                    (4,"⭐⭐⭐⭐ 4"),
                    (5,"⭐⭐⭐⭐⭐ 5"),
                ],

                attrs={
                    "class":"form-control"
                }

            ),

            "review": forms.Textarea(

                attrs={
                    "class":"form-control",
                    "rows":5,
                    "placeholder":"Share your experience..."
                }

            )

        }
