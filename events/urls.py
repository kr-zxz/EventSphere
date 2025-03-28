from django.urls import path
from django.contrib.auth.views import LogoutView


from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('about/', views.about, name='about'),

    #admin
    path('events/categories/', views.manage_categories, name='manage_categories'),
    path('events/categories/add/', views.add_category, name='add_category'),
    path('events/categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('events/categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    # Subcategories
    path('events/subcategories/', views.manage_subcategories, name='manage_subcategories'),
    path('events/subcategories/add/', views.add_subcategory, name='add_subcategory'),
    path('events/subcategories/edit/<int:subcategory_id>/', views.edit_subcategory, name='edit_subcategory'),
    path('events/subcategories/delete/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),


    path('events/', views.manage_events, name='manage_events'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),

    path('events/list/', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/category/<int:category_id>/', views.event_list_by_category, name='event_list_by_category'),
    path('events/book/<int:event_id>/', views.book_event, name='book_event'),

    # path('chatbot/', views.chatbot_page, name='chatbot_page'),
    # path('chatbot_api/', views.chatbot, name='chatbot_api'),

    # path('booking/', views.booking_page, name='booking_page'),
    # path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    # path('invoice/<int:booking_id>/', views.download_invoice, name='download_invoice'),

    # path('bookings/', views.admin_booking_list, name='admin_booking_list'),


    # path('bookings/', views.admin_booking_list, name='admin_booking_list'),
    
    # # URL pattern for generating the invoice
    # path('invoice/<int:booking_id>/', views.generate_invoice, name='generate_invoice'),
    
    path('booking/', views.booking_page, name='booking_page'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    # path('invoice/<int:booking_id>/', views.download_invoice, name='download_invoice'),
    path('bookings/', views.admin_booking_list, name='admin_booking_list'),
    # path("payment/<int:booking_id>/success/", views.payment_success, name="payment_success"),

    # path('booking/', views.booking_page, name='booking_page'),
    # path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    # path('invoice/<int:booking_id>/', views.download_invoice, name='download_invoice'),
    
    #razer api
    path("payment/<int:booking_id>/", views.payment_page, name="payment_page"),
    path("razorpay_callback/", views.razorpay_callback, name="razorpay_callback"),
    path("payment_success/<int:booking_id>/", views.payment_success, name="payment_success"),
    # path("download-invoice/<int:booking_id>/", views.download_invoice, name="download_invoice"),
 
    path("payment-history/", views.user_payment_history, name="user_payment_history"),
    path("download-invoice/<int:payment_id>/", views.download_invoice, name="download_invoice"),

   
    # path('admin/bookings/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('bookings/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('bookings/waiting/<int:booking_id>/', views.waiting_booking, name='waiting_booking'),
    path('booking-history/', views.booking_history, name='booking_history'),
    path('chatbot/', views.chatbot_ai, name='chatbot'),

    

    #wish
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:event_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('submit_review/<int:booking_id>/', views.submit_review, name='submit_review'),
    path('reviews/', views.admin_review_list, name='admin_review_list'),
    path('review/delete/<int:review_id>/',views.delete_review, name='delete_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),

    

    

    

    
    path('sales-report/', views.sales_report, name='sales_report'),
    path('attendance-report/', views.attendance_report, name='attendance_report'),
    path('event-charts/', views.event_charts, name='event_charts'),
    path('analytics/', views.admin_analytics, name='admin_analytics'),
    # path("chatbot/", views.chatbot_ai, name="chatbot_ai"),
    path('payments-history/', views.admin_payment_history, name='admin_payment_history'),
    
    


    
]




