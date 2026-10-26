
from django import forms


class StudentLinkRequestForm(forms.Form):
    admission_number = forms.CharField(
        label="Student admission number",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter admission number",
                "autocomplete": "off",
            }
        ),
    )

    full_name = forms.CharField(
        label="Student's full name",
        max_length=350,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter the student's full name",
                "autocomplete": "name",
            }
        ),
    )

class StudentAccessForm(forms.Form):
    admission_number = forms.CharField(
        label="Student admission number",
        max_length=50,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your admission number",
            "autocomplete": "off",
        }),
    )

    full_name = forms.CharField(
        label="Full name",
        max_length=350,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your full name",
            "autocomplete": "name",
        }),
    )


