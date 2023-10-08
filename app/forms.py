from django import forms

from app.models import Student


class LogForm(forms.Form):
    serial_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Student Serial Number",
                "autofocus": True,
            }
        ),
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        serial_number = cleaned_data.get("serial_number")
        try:
            student = Student.objects.get(serial_number=serial_number)
            cleaned_data["name"] = student.name
        except Student.DoesNotExist:
            raise forms.ValidationError("Student with given serial number does not exist.")
        return cleaned_data
