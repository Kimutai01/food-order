from django.shortcuts import render

# Create your views here.

def c_profile(request):
    return render(request, 'customer/cprofile.html')
