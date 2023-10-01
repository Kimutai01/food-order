from django.conf import settings

def get_google_api(request):
    return {
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
    }
    
def get_paypal_client_id(request):
    return {
        'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID
    }