from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Booking, EventCategory, EventSubCategory, Event

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(EventSubCategory)
class EventSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    search_fields = ('name',)
    list_filter = ('category',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'subcategory', 'location', 'date', 'package_amount')
    search_fields = ('title', 'category__name')
    list_filter = ('category', 'subcategory', 'location', 'date')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_date', 'event_type', 'phone_number', 'advance_paid']
    search_fields = ['user__username', 'email']

from django.contrib import admin
from .models import Review

from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'rating', 'sentiment', 'created_at')  # Add 'sentiment' to list_display
    list_filter = ('rating', 'event', 'sentiment')  # Add 'sentiment' to list_filter
    search_fields = ('user__username', 'event__title', 'comment')

admin.site.register(Review, ReviewAdmin)


from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'booking', 'payment_method', 'transaction_id', 'status', 'payment_date')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'transaction_id', 'razorpay_order_id')
