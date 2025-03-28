# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='profile_images/', default='default_profile.png')  # Add this field

    def __str__(self):
        return self.user.username


#admin events list

from django.db import models

class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class EventSubCategory(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    


class Event(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='events')
    subcategory = models.ForeignKey(EventSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    location = models.TextField()
    date = models.DateField()
    package_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


#booking

from django.db import models
from django import forms
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import admin

#from django.db import models
from django.contrib.auth.models import User

# Booking Model
# models.py
from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
        ('Waiting', 'Waiting'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Remove null=True

    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    event_date = models.DateField()
    event_type = models.CharField(max_length=100)
    location_details = models.TextField()
    pincode = models.CharField(max_length=6)
    food_options = models.BooleanField(default=False)
    advice = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50)
    advance_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Waiting')


    def __str__(self):
        return f"Booking by {self.user.username} for {self.event.title} on {self.event_date}"

from django.db import models
from django.contrib.auth.models import User
from .models import Event

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

#review and rating
from django.db import models

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(default="No comment")
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=10, blank=True, null=True)  # New field for sentiment

    def __str__(self):
        return f"Review by {self.user.username} for {self.event.title} - {self.rating} Stars"


#payment
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Booking

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('UPI', 'UPI'),
        ('Credit Card', 'Credit Card'),
        ('Razorpay', 'Razorpay'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    
    # ✅ Razorpay Fields
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)  
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)  

    payment_status = models.BooleanField(default=False)  # ✅ True if payment is successful
    status = models.CharField(
        max_length=20, 
        choices=[("Pending", "Pending"), ("Success", "Success"), ("Failed", "Failed")], 
        default="Pending"
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - {self.payment_method}"
