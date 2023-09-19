from django.shortcuts import render, HttpResponse, redirect
from .forms import UserForm, ProfileForm
from django.contrib import messages
from vendor.forms import VendorForm
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib import auth
from .utils import send_verification_email, detect_user
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from vendor.models import Vendor
from vendor.models import OpeningHour, Appointment
from django.shortcuts import get_object_or_404

# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = user.CUSTOMER
            user.set_password(password)
            user.save()
            
            # send verification email
            subject = 'Please activate your account'
            template = 'activate_account.html'
            send_verification_email(request,user,subject,template)
            messages.success(request, 'Your account has been created successfully')
            return redirect('register-user')
        else:
            print('Form is not valid')
            print(form.errors)
    else:
        form = UserForm()
    
    context = {
        'form': form
    }
    return render(request, 'registerUser.html', context)

def registerVendor(request):
    form = UserForm()
    vendorForm = VendorForm()
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        vendorForm = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendorForm.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = user.CLINIC
            user.set_password(password)
            user.save()
            vendor = vendorForm.save(commit=False)
            vendor.user = user
            profile = Profile.objects.get(user=user)
            vendor.profile = profile
            vendor.save()
            subject = 'Please activate your account'
            template = 'activate_account.html'
            send_verification_email(request,user,subject,template)
            messages.success(request, 'Your account has been created successfully, please wait for the approval')
            return redirect('register-vendor')
        else:
            print('Form is not valid')
            print(form.errors)
            print(vendorForm.errors)
    else:
        form = UserForm()
        vendorForm = VendorForm()
    context = {
        'form': form,
        'vendorForm': vendorForm,
        
    }
    return render(request, 'registerVendor.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are now logged out')
    return redirect('login')