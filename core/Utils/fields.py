from django import forms
from django.core.validators import RegexValidator


class PhoneField(forms.CharField):
    phone_validator = RegexValidator(regex=r'^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$',
                                     message=(
                                         "Phone number must be entered in the format: '+380(99)-999-9999'."))

    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(self.phone_validator)
