from django import forms


from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'country', 'county', 'city']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'last_name': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'email': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'phone': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'address': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'country': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'county': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
            'city': forms.TextInput(attrs={'class': 'h-10 border mt-1 rounded px-4 w-full bg-gray-50'}),
        }