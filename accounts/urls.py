from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.myAccount, name='myAccount'),
    path('registerUser/', views.registerUser, name='register-user'),
    path('registerVendor/', views.registerVendor, name='register-vendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('customerBookings/', views.customer_booking, name='customer-booking'),
    path('restaurantDashboard/', views.restaurantDashboard, name='restaurantDashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('restaurant/', include('vendor.urls')),
    path('profile/edit_customer/', views.edit_customer_profile, name='edit_customer'),
    
    path('customers/', include('customers.urls')),
    
]
