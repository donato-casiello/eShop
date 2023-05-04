from django import forms 
from django.forms.widgets import FileInput

from django_countries.fields import CountryField


PAYMENT_CHOICES = (
        ('S', "Stripe"),
        ('P', "PayPal"),
    )

class CheckoutForm(forms.Form):
    street_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "placeholder":"1234 Main St", 
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "placeholder":"Apartment or suite"
    }))
    country = CountryField(blank_label='Select Country').formfield()
    cap = forms.CharField(required=True, widget=forms.TextInput())
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

# Create a custom datefield input
class DateInput(forms.DateInput):
    input_type = "date"
    
class EditProfileForm(forms.Form):
    profile_image = forms.ImageField(required=False, widget=FileInput(), label="Change profile image")
    first_name = forms.CharField(label="First Name", required=False, widget=forms.TextInput())
    last_name = forms.CharField(required=False, widget=forms.TextInput())
    mobile_number = forms.CharField(required=False, max_length=10)
    address = forms.CharField(required=False, max_length=100)
    birthday = forms.DateField(required=False, widget=DateInput())
    state = CountryField(blank_label="Select Country").formfield()
    
    
    
    # To set required=False in state field
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['state'].required = False
