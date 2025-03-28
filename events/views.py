from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')



#user login/Registations
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import BookingForm, UserRegistrationForm
from django.contrib.auth.models import User
from .models import Booking, UserProfile 
from django.core.mail import send_mail
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check if the email is already registered
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email is already registered. Please log in.")
                return render(request, 'register.html', {'form': form})

            # Create user
            user = User.objects.create_user(
                username=email,
                password=password
            )

            # Create the profile
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                email=email,
                mobile_number=form.cleaned_data['mobile_number'],
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender']
            )

            # Send Registration Success Email
            subject = "Welcome to Evento - Registration Successful!"
            message = f"Hi {form.cleaned_data['full_name']},\n\nThank you for registering at Evento! You can now log in and start booking events.\n\nBest Regards,\nEvento Team"
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Registration successful. Check your email for confirmation.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

# Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')  # Redirect after successful login
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


#logut
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')  # Redirect to the home page after logout




#profile 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile, Booking  # Ensure Booking is imported

@login_required
def profile(request):
    """View to display the logged-in user's profile and their bookings."""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('home')

    # Fetch all bookings associated with the logged-in user
    user_bookings = Booking.objects.filter(user=request.user).order_by('-event_date')
  # Sort by recent bookings

    context = {
        'user_profile': user_profile,
        'user_bookings': user_bookings,
    }
    return render(request, 'profile.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)  # Handle file uploads
        if form.is_valid():
            # Update user details
            user = user_profile.user
            user.username = form.cleaned_data['email']  # Update username
            user.set_password(form.cleaned_data['password'])  # Update password
            user.save()
            form.save()  # Save the UserProfile instance
            messages.success(request, "Your profile has been updated.")
            return redirect('login')  # Redirect to login page after update
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})


# #admindashboards
# # views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Admin Login View

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class AdminLoginView(LoginView):
    template_name = 'admin_login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        print(self.request.user.is_superuser)  # Debug line
        if self.request.user.is_superuser:
            return reverse_lazy('admin_dashboard')  # Redirect to admin dashboard
        return reverse_lazy('home')  # Redirect to home

# Admin Dashboard View
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_events = Event.objects.count()
    total_bookings = Booking.objects.count()
    total_revenue = sum(booking.event.package_amount for booking in Booking.objects.filter(status="Approved"))

    recent_bookings = Booking.objects.all().order_by('-event_date')[:5]

    context = {
        "total_users": total_users,
        "total_events": total_events,
        "total_bookings": total_bookings,
        "total_revenue": total_revenue,
        "recent_bookings": recent_bookings,
    }
    return render(request, 'admin_dashboard.html', context)


#admin events 

from django.shortcuts import render, redirect, get_object_or_404
from .models import EventCategory, EventSubCategory, Event
from .forms import EventCategoryForm, EventForm

# Category Management
def manage_categories(request):
    categories = EventCategory.objects.all()
    return render(request, 'manage_categories.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = EventCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = EventCategoryForm()
    return render(request, 'add_category.html', {'form': form})

def edit_category(request, category_id):
    category = get_object_or_404(EventCategory, id=category_id)
    if request.method == 'POST':
        form = EventCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = EventCategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(EventCategory, id=category_id)
    category.delete()
    return redirect('manage_categories')

# Event Management
def manage_events(request):
    events = Event.objects.all()
    return render(request, 'manage_events.html', {'events': events})

from django.shortcuts import render, redirect
from .models import EventCategory, EventSubCategory
from .forms import EventForm

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Replace 'event_list' with the appropriate URL name
    else:
        form = EventForm()

    # Fetch categories and subcategories from the database
    categories = EventCategory.objects.all()
    subcategories = EventSubCategory.objects.all()

    return render(request, 'add_event.html', {
        'form': form,
        'categories': categories,
        'subcategories': subcategories,
    })

# def edit_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES, instance=event)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_events')
#     else:
#         form = EventForm(instance=event)
#     return render(request, 'edit_event.html', {'form': form})

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    categories = EventCategory.objects.all()
    subcategories = EventSubCategory.objects.all()
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('manage_events')
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'categories': categories,
        'subcategories': subcategories
    }
    return render(request, 'edit_event.html', context)


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('manage_events')


#user event lists

from django.contrib.auth.decorators import login_required
from .models import Event
from django.shortcuts import render, get_object_or_404
from .models import Event, EventCategory



from django.shortcuts import render, get_object_or_404
from .models import Event, EventCategory

from django.shortcuts import render, get_object_or_404
from .models import EventCategory, Event


@login_required
def event_list(request):
    query = request.GET.get('q', '')  # Get the search query
    categories = EventCategory.objects.all()

    if query:
        events = Event.objects.filter(title__icontains=query)  # Search events by title
    else:
        events = Event.objects.all()

    context = {
        'categories': categories,
        'events': events,
        'query': query,  # Include query for preserving the input value
    }
    return render(request, 'event_list.html', context)



def event_list_by_category(request, category_id):
    categories = EventCategory.objects.all()
    category = get_object_or_404(EventCategory, id=category_id)
    events = Event.objects.filter(category=category)
    context = {
        'categories': categories,
        'events': events,
        'selected_category': category,
    }
    return render(request, 'event_list.html', context)


# from django.shortcuts import render, get_object_or_404
# from .models import Event

# def event_detail(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     return render(request, 'event_detail.html', {'event': event})

from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Event, Review

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = Review.objects.filter(event=event).order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0  # Calculate avg rating

    return render(request, 'event_detail.html', {
        'event': event,
        'reviews': reviews,
        'average_rating': round(average_rating, 1)  # Round to 1 decimal place
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages

#wishlist
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Wishlist
from django.contrib import messages

@login_required
def add_to_wishlist(request):
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        
        # Check if the event is already in the wishlist
        if not Wishlist.objects.filter(user=request.user, event=event).exists():
            Wishlist.objects.create(user=request.user, event=event)
            messages.success(request, "Event added to your wishlist!")
        else:
            messages.info(request, "This event is already in your wishlist.")
        
        return redirect('wishlist')  # Redirect to the wishlist page
    return redirect('home')  # Redirect to home if request is not POST

def remove_from_wishlist(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, event=event).first()
    
    if wishlist_item:
        wishlist_item.delete()
        return redirect('wishlist')  # Redirect back to the wishlist page

    return redirect('wishlist')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Add your booking logic here
    messages.success(request, f"You have successfully booked the event: {event.title}")
    return redirect('event_list')


import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Your Gemini API Key (Replace with your actual API key)
GEMINI_API_KEY = '#'

# Function to interact with the Gemini API
def get_gemini_response(user_input):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": user_input}]}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract chatbot response
        if "candidates" in data and len(data["candidates"]) > 0:
            bot_message = data["candidates"][0]["output"]
        else:
            bot_message = "Sorry, I couldn't understand your request."

        return {"response": bot_message}

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"response": "Sorry, there was an error with the chatbot. Please try again later."}

# View for rendering chatbot page
def chatbot_page(request):
    return render(request, 'chatbot_page.html')

# API endpoint to receive chatbot messages
@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message', '')

            if user_input:
                gemini_response = get_gemini_response(user_input)
                return JsonResponse({"response": gemini_response["response"]})
            else:
                return JsonResponse({"response": "No message received."}, status=400)

        except Exception as e:
            print(f"Error handling request: {e}")
            return JsonResponse({"response": "An error occurred. Please try again later."}, status=500)

    return JsonResponse({"response": "Invalid request method."}, status=400)


#subcategoire views

from .models import EventSubCategory
from .forms import EventSubCategoryForm

# Subcategory Management
def manage_subcategories(request):
    subcategories = EventSubCategory.objects.all()
    return render(request, 'manage_subcategories.html', {'subcategories': subcategories})

from .models import EventCategory

def add_subcategory(request):
    categories = EventCategory.objects.all()  # Fetch all categories
    if request.method == 'POST':
        form = EventSubCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_subcategories')
    else:
        form = EventSubCategoryForm()
    return render(request, 'add_subcategory.html', {'form': form, 'categories': categories})


def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(EventSubCategory, id=subcategory_id)
    if request.method == 'POST':
        form = EventSubCategoryForm(request.POST, request.FILES, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('manage_subcategories')
    else:
        form = EventSubCategoryForm(instance=subcategory)
    return render(request, 'edit_subcategory.html', {'form': form})

def delete_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(EventSubCategory, id=subcategory_id)
    subcategory.delete()
    return redirect('manage_subcategories')


#booking form # User Booking Page

# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
# from .models import Booking, Event
# from .forms import BookingForm
# from django.template.loader import render_to_string

# @login_required
# def booking_page(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.advance_paid = True  # Assume advance is always paid
#             booking.save()
#             messages.success(request, "Your booking was successful!")
#             return redirect('payment_page', booking_id=booking.id)
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = BookingForm()

#     return render(request, 'booking_form.html', {'form': form})

# # Payment Page
# def payment_page(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     return render(request, 'payment_page.html', {'booking': booking})

# # Download Invoice
# def download_invoice(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     html_content = render_to_string('invoice.html', {'booking': booking})
#     response = HttpResponse(html_content, content_type='text/html')
#     response['Content-Disposition'] = f'attachment; filename="invoice_{booking_id}.html"'
#     return response

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import get_template
from .models import Booking, Event
from django.conf import settings
from xhtml2pdf import pisa
import os

# Booking Page
@login_required
def booking_page(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.advance_paid = True  # Assume payment is required
            booking.save()
            messages.success(request, "Your booking was successful! Proceed to payment.")
            return redirect('payment_page', booking_id=booking.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form})


# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
# from django.template.loader import get_template
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.conf import settings
# from reportlab.pdfgen import canvas
# from .models import Event, Booking, Payment
# from django.contrib.auth.decorators import login_required

# @login_required
# def payment_page(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     event = booking.event  

#     if request.method == "POST":
#         payment_method = request.POST.get("payment_method")
#         upi_id = request.POST.get("upi_id", "")
#         card_number = request.POST.get("card_number", "")
#         card_expiry = request.POST.get("card_expiry", "")
#         card_cvv = request.POST.get("card_cvv", "")

#         # Create Payment object
#         payment = Payment.objects.create(
#             booking=booking,
#             user=request.user,
#             payment_method=payment_method,
#             upi_id=upi_id if payment_method == "UPI" else None,
#             card_number=card_number if payment_method == "Credit Card" else None,
#             card_expiry=card_expiry if payment_method == "Credit Card" else None,
#             card_cvv=card_cvv if payment_method == "Credit Card" else None,
#             status="Success"
#         )

#         # ✅ Send Confirmation Email
#         subject = "Payment Successful - Event Booking"
#         message = f"Dear {request.user.username},\n\nYour payment for the event '{event.title}' was successful.\n\nAmount Paid: ₹{event.package_amount}\n\nThank you!"
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [request.user.email])

#         # ✅ Show success notification
#         messages.success(request, "Payment successful! You will receive a confirmation email.")

#         # ✅ Redirect to actual payment_success page
#         return redirect("payment_success", booking_id=booking.id)

#     return render(request, "payment_integration.html", {"booking": booking, "event": event})

# @login_required
# def payment_success(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     event = booking.event
#     payment = Payment.objects.filter(booking=booking).last()

#     return render(request, "payment_success.html", {"booking": booking, "event": event, "payment": payment})

# from django.shortcuts import get_object_or_404
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from .models import Booking, Payment

# from django.utils import timezone

# @login_required
# def download_invoice(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     event = booking.event
#     payment = Payment.objects.filter(booking=booking).last()  # Get latest payment

#     response = HttpResponse(content_type="application/pdf")
#     response["Content-Disposition"] = f'attachment; filename="invoice_{booking.id}.pdf"'

#     pdf = SimpleDocTemplate(response, pagesize=letter)
#     elements = []

#     # Invoice data
#     data = [
#         ["Invoice for Booking", ""],
#         ["Booking ID", booking.id],
#         ["Event Name", event.title],
#         ["Event Date", event.date.strftime("%b. %d, %Y")],
#         ["User", booking.user.email],
#         ["Payment Method", payment.payment_method if payment else "N/A"],
#         ["Transaction ID", payment.id if payment else "N/A"],
#         ["Amount Paid", f"₹{event.package_amount}" if payment else "N/A"],
#         ["Payment Date", timezone.now().strftime("%b. %d, %Y") if payment else "N/A"],  # Use current time
#     ]

#     # Table styling
#     table = Table(data, colWidths=[150, 300])
#     table.setStyle(
#         TableStyle([
#             ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
#             ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
#             ("ALIGN", (0, 0), (-1, -1), "LEFT"),
#             ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#             ("FONTSIZE", (0, 0), (-1, -1), 12),
#             ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
#             ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
#             ("GRID", (0, 0), (-1, -1), 1, colors.black),
#         ])
#     )

#     elements.append(table)
#     pdf.build(elements)

#     return response

import razorpay
import json
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .models import Booking, Payment

# ✅ STEP 1: Show Payment Page
@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    event = booking.event  
    amount = int(event.package_amount * 100)  # Convert ₹ to paisa

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # ✅ Create Razorpay Order
    order_data = {
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1",  # Auto-capture payment
    }
    order = client.order.create(order_data)

    # ✅ Save Initial Payment Record (Pending)
    Payment.objects.create(
        user=booking.user,
        booking=booking,
        payment_method="Razorpay",
        razorpay_order_id=order["id"],
        payment_status=False,  
        status="Pending",
    )

    context = {
        "booking": booking,
        "event": event,
        "razorpay_order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
    }
    return render(request, "payment_integration.html", context) 

# ✅ STEP 2: Razorpay Callback for Payment Verification
@csrf_exempt
def razorpay_callback(request):
    if request.method == "POST":
        data = json.loads(request.body)
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        payment = Payment.objects.filter(razorpay_order_id=razorpay_order_id).first()
        if not payment:
            return JsonResponse({"status": "error", "message": "Payment record not found!"})

        try:
            # ✅ Verify Payment Signature
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })

            # ✅ Update Payment Record
            payment.transaction_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.payment_status = True  
            payment.status = "Success"
            payment.payment_date = timezone.now()
            payment.save()

            # ✅ Generate Invoice
            invoice_path = generate_invoice_pdf(payment.booking, payment)

            # ✅ Send Confirmation Email with Invoice
            send_invoice_email(payment.user.email, invoice_path)

            return JsonResponse({"status": "success", "redirect_url": f"/payment_success/{payment.booking.id}/"})

        except razorpay.errors.SignatureVerificationError:
            payment.status = "Failed"
            payment.save()
            return JsonResponse({"status": "error", "message": "Payment verification failed!"})


# ✅ STEP 3: Payment Success Page & Invoice Download
@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment = Payment.objects.filter(booking=booking, status="Success").last()  

    if not payment:
        messages.error(request, "Payment not found or not successful.")
        return redirect("homepage")

    invoice_path = f"/media/invoices/invoice_{booking.id}.pdf"

    messages.success(request, "Payment successful! You can download your invoice below.")
    return render(request, "payment_success.html", {"booking": booking, "payment": payment, "invoice_path": invoice_path})


# ✅ STEP 4: Generate Invoice PDF
def generate_invoice_pdf(booking, payment):
    invoice_dir = os.path.join(settings.MEDIA_ROOT, "invoices")
    os.makedirs(invoice_dir, exist_ok=True)

    pdf_path = os.path.join(invoice_dir, f"invoice_{booking.id}.pdf")
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []

    data = [
        ["Invoice for Booking", ""],
        ["Booking ID", booking.id],
        ["Event Name", booking.event.title],
        ["Event Date", booking.event.date.strftime("%b. %d, %Y")],
        ["User", booking.user.email],
        ["Payment Method", payment.payment_method],
        ["Transaction ID", payment.transaction_id],
        ["Amount Paid", f"₹{booking.event.package_amount}"],
        ["Payment Date", timezone.now().strftime("%b. %d, %Y")], 
    ]

    table = Table(data, colWidths=[150, 300])
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
    )

    elements.append(table)
    pdf.build(elements)

    return pdf_path  


# ✅ STEP 6: Download Invoice
@login_required
def download_invoice(request, booking_id):
    pdf_path = os.path.join(settings.MEDIA_ROOT, "invoices", f"invoice_{booking_id}.pdf")

    if os.path.exists(pdf_path):
        return FileResponse(open(pdf_path, "rb"), as_attachment=True, filename=f"invoice_{booking_id}.pdf")
    else:
        messages.error(request, "Invoice not found.")
        return redirect("payment_success", booking_id=booking_id)




# Admin Booking List
def admin_booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'admin_booking_list.html', {'bookings': bookings})

# views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Booking

# Send email notification
def send_booking_email(booking, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        fail_silently=False,
    )

# Confirm action before updating booking status
def confirm_action(request, booking_id, status):
    return JsonResponse({
        "message": f"Are you sure you want to {status.lower()} booking ID {booking_id}?",
        "status": status,
        "booking_id": booking_id
    })

# Update booking status
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = status
    booking.save()
    messages.success(request, f"Booking ID {booking.id} status updated to {status}.")

    subject = f"Your Booking #{booking.id} Status Updated"
    message = f"Dear {booking.user.username},\n\nYour booking for {booking.event.title} has been updated to: {status}.\n\nThank you for using our service."
    send_booking_email(booking, subject, message)
    
    return redirect('admin_booking_list')

# Approve booking
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Approved'
    booking.save()
    messages.success(request, "Booking approved successfully.")

    subject = "Your Booking Has Been Approved"
    message = f"Dear {booking.user.username},\n\nYour booking for {booking.event.title} has been approved.\n\nThank you for using our service."
    send_booking_email(booking, subject, message)
    
    return redirect('admin_booking_list')

# Cancel booking
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Cancelled'
    booking.save()
    messages.success(request, "Booking cancelled successfully.")

    subject = "Your Booking Has Been Cancelled"
    message = f"Dear {booking.user.username},\n\nYour booking for {booking.event.title} has been cancelled.\n\nIf you have any questions, please contact support."
    send_booking_email(booking, subject, message)
    
    return redirect('admin_booking_list')

# Set booking to waiting
def waiting_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Waiting'
    booking.save()
    messages.success(request, "Booking status set to waiting.")

    subject = "Your Booking is in Waiting Status"
    message = f"Dear {booking.user.username},\n\nYour booking for {booking.event.title} is currently in waiting status.\n\nWe will notify you once it is updated."
    send_booking_email(booking, subject, message)
    
    return redirect('admin_booking_list')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking

@login_required
def booking_history(request):
    """View to display the logged-in user's booking history."""
    user_bookings = Booking.objects.filter(user=request.user).order_by('-event_date')
    context = {
        'user_bookings': user_bookings,
    }
    return render(request, 'booking_history.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking

@login_required
def booking_history(request):
    """View to display the logged-in user's booking history."""
    user_bookings = Booking.objects.filter(user=request.user).order_by('-event_date')
    context = {
        'user_bookings': user_bookings,
    }
    return render(request, 'booking_history.html', context)


#adminchart
# views.py
from django.shortcuts import render
from .models import Booking, Event
import plotly.express as px
import pandas as pd

from django.shortcuts import render
from django.db.models import Sum
from .models import Booking

def sales_report(request):
    # Fetch all bookings
    bookings = Booking.objects.all()
    
    # Calculate total amount from all bookings
    total_amount = bookings.aggregate(Sum('event__package_amount'))['event__package_amount__sum'] or 0
    
    context = {
        'bookings': bookings,
        'total_amount': total_amount,
    }
    return render(request, 'sales_report.html', context)
def attendance_report(request):
    # Fetch all bookings
    bookings = Booking.objects.all()
    context = {
        'bookings': bookings,
    }
    return render(request, 'attendance_report.html', context)

def event_charts(request):
    # Generate charts using Plotly
    events = Event.objects.all()
    df = pd.DataFrame(list(events.values('title', 'date', 'package_amount')))
    fig = px.bar(df, x='title', y='package_amount', title='Event Package Amounts')
    chart = fig.to_html(full_html=False)

    context = {
        'chart': chart,
    }
    return render(request, 'event_charts.html', context)

#review


# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Booking, Review, Event
# from django.http import JsonResponse

# @login_required
# def submit_review(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id, user=request.user)

#     # Ensure the booking is approved before reviewing
#     if booking.status != 'Approved':
#         messages.error(request, "You can only review approved events.")
#         return redirect('booking_history')

#     if request.method == "POST":
#         rating = int(request.POST.get("rating"))
#         comment = request.POST.get("comment")

#         # Ensure review is linked to the specific booking
#         existing_review = Review.objects.filter(user=request.user, event=booking.event, booking=booking).first()

#         if existing_review:
#             existing_review.rating = rating
#             existing_review.comment = comment
#             existing_review.save()
#             messages.success(request, "Your review has been updated!")
#         else:
#             Review.objects.create(user=request.user, event=booking.event, booking=booking, rating=rating, comment=comment)
#             messages.success(request, "Thank you for your review!")

#         return JsonResponse({"message": "Review submitted successfully", "rating": rating, "comment": comment})

#     return redirect('booking_history')

#review ai
from textblob import TextBlob  # Import TextBlob for sentiment analysis

@login_required
def submit_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != 'Approved':
        messages.error(request, "You can only review approved events.")
        return redirect('booking_history')

    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(comment)
        sentiment = "positive" if analysis.sentiment.polarity > 0 else "negative" if analysis.sentiment.polarity < 0 else "neutral"

        existing_review = Review.objects.filter(user=request.user, event=booking.event, booking=booking).first()

        if existing_review:
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.sentiment = sentiment  # Update sentiment
            existing_review.save()
            messages.success(request, "Your review has been updated!")
        else:
            Review.objects.create(
                user=request.user,
                event=booking.event,
                booking=booking,
                rating=rating,
                comment=comment,
                sentiment=sentiment  # Save sentiment
            )
            messages.success(request, "Thank you for your review!")

        return JsonResponse({"message": "Review submitted successfully", "rating": rating, "comment": comment, "sentiment": sentiment})

    return redirect('booking_history')

#admin review list show

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Review

# Check if user is an admin
def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_review_list(request):
    """View to display all user reviews for admins."""
    reviews = Review.objects.all().order_by('-created_at')  # Fetch reviews in descending order
    return render(request, 'admin_review_list.html', {'reviews': reviews})

from django.http import JsonResponse

@user_passes_test(is_admin)
def delete_review(request, review_id):
    """Allows an admin to delete a review and sends a JSON response."""
    if request.method == "POST":
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return JsonResponse({"success": True})  # ✅ Return JSON response
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)



#analytics

from django.shortcuts import render
from django.db.models import Count, Sum, Avg
from .models import Booking, Event, Review

def admin_analytics(request):
    # Fetch event-wise bookings count
    event_data = Event.objects.annotate(total_bookings=Count('booking'))
    event_names = [event.title for event in event_data]
    event_bookings = [event.total_bookings for event in event_data]

    # Fetch event-wise revenue
    event_revenue = []
    for event in event_data:
        revenue = Booking.objects.filter(event=event, status='Approved').aggregate(total_revenue=Sum('event__package_amount'))['total_revenue']
        event_revenue.append(revenue if revenue else 0)

    # Fetch rating distribution
    ratings = Review.objects.values('rating').annotate(count=Count('rating')).order_by('rating')
    rating_counts = [0, 0, 0, 0, 0]  # Default list for 1-5 stars
    for rating in ratings:
        rating_counts[rating['rating'] - 1] = rating['count']

    context = {
        'event_names': event_names,
        'event_bookings': event_bookings,
        'event_revenue': event_revenue,
        'rating_counts': rating_counts
    }

    return render(request, 'admin_analytics.html', context)


from django.shortcuts import render

def about(request):
    return render(request, 'about.html')




# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import google.generativeai as genai

# # ✅ Configure Gemini API
# GEMINI_API_KEY = "#"  # Replace with your valid API key
# genai.configure(api_key=GEMINI_API_KEY)

# try:
#     # ✅ Use the correct model name
#     model = genai.GenerativeModel("gemini-1.0-pro")
# except Exception as e:
#     print(f"Model initialization failed: {e}")
#     model = None

# @csrf_exempt
# def chatbot_ai(request):
#     if request.method == "POST":
#         try:
#             # ✅ Parse JSON request from frontend
#             data = json.loads(request.body)
#             user_input = data.get("message", "").strip()

#             if not user_input:
#                 return JsonResponse({"response": "No input provided."}, status=400)

#             if not model:
#                 return JsonResponse({"response": "Gemini API model is missing or invalid."}, status=500)

#             # ✅ Generate chatbot response
#             response = model.generate_content([user_input])

#             # ✅ Ensure valid response
#             bot_reply = response.text.strip() if hasattr(response, "text") else "Sorry, I couldn't generate a response."

#             return JsonResponse({"response": bot_reply})

#         except json.JSONDecodeError:
#             return JsonResponse({"response": "Invalid JSON format."}, status=400)
#         except Exception as e:
#             return JsonResponse({"response": f"Error: {str(e)}"}, status=500)

#     return render(request, "chatbot.html")

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from .models import Payment

@staff_member_required
def admin_payment_history(request):
    """View to display all payment history for admin."""
    payments = Payment.objects.select_related('user', 'booking__event').order_by('-payment_date')
    
    # ✅ Ensure correct field for total calculation
    total_amount = payments.aggregate(total=Sum('booking__event__package_amount'))['total'] or 0

    context = {
        'payments': payments,
        'total_amount': total_amount,
    }
    return render(request, 'admin_payment_history.html', context)




from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

# ✅ Configure Gemini API
GEMINI_API_KEY = "AIzaSyCXf5nEA7kIXwn7ypCzU9fuesLCHO3qXEo"  # Replace with your valid API key
genai.configure(api_key=GEMINI_API_KEY)

try:
    # ✅ Use the correct model name
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    print(f"Model initialization failed: {e}")
    model = None

@csrf_exempt
def chatbot_ai(request):
    if request.method == "POST":
        try:
            # ✅ Parse JSON request from frontend
            data = json.loads(request.body)
            user_input = data.get("message", "").strip()

            if not user_input:
                return JsonResponse({"response": "No input provided."}, status=400)

            if not model:
                return JsonResponse({"response": "Gemini API model is missing or invalid."}, status=500)

            # ✅ Generate chatbot response
            response = model.generate_content([user_input])

            # ✅ Ensure valid response
            bot_reply = response.text.strip() if hasattr(response, "text") else "Sorry, I couldn't generate a response."

            return JsonResponse({"response": bot_reply})

        except json.JSONDecodeError:
            return JsonResponse({"response": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"response": f"Error: {str(e)}"}, status=500)

    return render(request, "chatbot.html")


import os
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.contrib import messages
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from django.core.paginator import Paginator 
from .models import Payment


@login_required
def user_payment_history(request):
    """Displays user's payment history with pagination."""
    payments = Payment.objects.filter(user=request.user).order_by('-payment_date')

    paginator = Paginator(payments, 5)  # Show 5 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'payments': page_obj,
        'total_payments': payments.count(),
    }

    return render(request, 'user_payment_history.html', context)


@login_required
def download_invoice(request, payment_id):
    """Generate and download a PDF invoice for successful payments."""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    # Ensure only successful payments have invoices
    if payment.status != "Success":
        messages.error(request, "Invoice is only available for successful payments.")
        return redirect("user_payment_history")

    # Create PDF in memory
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Invoice_{payment.booking.id}")

    # Set title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "EventSphere Payment Invoice")
    
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 720, f"Invoice ID: {payment.id}")
    pdf.drawString(50, 700, f"Transaction ID: {payment.transaction_id}")
    pdf.drawString(50, 680, f"Booking ID: {payment.booking.id}")
    pdf.drawString(50, 660, f"Event Name: {payment.booking.event.title}")
    pdf.drawString(50, 640, f"Payment Method: {payment.payment_method}")
    pdf.drawString(50, 620, f"Amount Paid: ₹{payment.booking.event.package_amount}")
    pdf.drawString(50, 600, f"Payment Date: {payment.payment_date.strftime('%Y-%m-%d %H:%M:%S')}")

    # Table data
    table_data = [
        ["Field", "Details"],
        ["Invoice ID", str(payment.id)],
        ["Transaction ID", payment.transaction_id if payment.transaction_id else "N/A"],
        ["Booking ID", str(payment.booking.id)],
        ["Event Name", payment.booking.event.title],
        ["Payment Method", payment.get_payment_method_display()],
        ["Amount Paid", f"₹{payment.booking.event.package_amount}"],
        ["Payment Date", payment.payment_date.strftime('%Y-%m-%d %H:%M:%S')],
        ["Status", payment.status]
    ]

    # Create table
    table = Table(table_data, colWidths=[150, 300])
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
    )

    # Draw table on PDF
    table.wrapOn(pdf, 400, 500)
    table.drawOn(pdf, 50, 500)

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"invoice_{payment.booking.id}.pdf")
