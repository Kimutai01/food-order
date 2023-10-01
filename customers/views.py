from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.forms import UserInfoForm, ProfileForm
from django.contrib import messages
from accounts.models import *
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

# Create your views here.
@login_required(login_url='login')
def c_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        customer_form = UserInfoForm(request.POST, instance=request.user)
        print(customer_form)
        if profile_form.is_valid() and customer_form.is_valid():
            profile_form.save()
            customer_form.save()
            messages.success(request, 'Profile updated')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(customer_form.errors)
    else:
        profile_form = ProfileForm(instance=profile)
        customer_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'customer_form': customer_form,
        'profile': profile,
    }
    return render(request, 'customer/cprofile.html', context)
