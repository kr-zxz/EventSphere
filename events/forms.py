from django import forms
from django.contrib.auth.models import User
from .models import Booking, EventSubCategory, UserProfile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'mobile_number', 'age', 'gender', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


#profile
# forms.py
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=False)

    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'mobile_number', 'age', 'gender', 'profile_image']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class AdminLoginForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')


#admin events

from django import forms
from .models import EventCategory, Event

class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ['name', 'description', 'image']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'subcategory', 'description', 'image', 'location', 'date', 'package_amount']


#subcategoirs
class EventSubCategoryForm(forms.ModelForm):
    class Meta:
        model = EventSubCategory
        fields = ['category', 'name','description']


from django.core.exceptions import ValidationError

from django import forms
from django.core.exceptions import ValidationError
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'event', 
            'phone_number', 
            'email', 
            'event_date', 
            'event_type', 
            'location_details', 
            'pincode', 
            'food_options', 
            'advice', 
            'payment_method'
        ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'event_type': forms.Select(choices=[
                ('Destination', 'Destination'), 
                ('Indoor', 'Indoor')
            ], attrs={'class': 'form-control'}),
            'location_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'food_options': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'payment_method': forms.Select(choices=[
                ('Cash', 'Cash'),
                ('Credit Card', 'Credit Card'),
                ('UPI', 'UPI'),
                ('Net Banking', 'Net Banking')
            ], attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValidationError("Please enter a valid 10-digit phone number.")
        return phone_number

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not pincode.isdigit() or len(pincode) != 6:
            raise ValidationError("Please enter a valid 6-digit pincode.")
        return pincode

    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        from datetime import date
        if event_date < date.today():
            raise ValidationError("Event date cannot be in the past.")
        return event_date

#payment formms.py
    
from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']  # ✅ Only include relevant fields
        
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        if payment_method not in ['UPI', 'Credit Card', 'Razorpay']:
            self.add_error('payment_method', 'Invalid payment method selected.')

        return cleaned_data
