from django import forms
from .models import User, Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password']
    
    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-4 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'}),
        'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'}),
        'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'}),
        'email': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'}),
    }
        
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "passwords do not match"
            )
        
   
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture','cover_picture','address','country','county','city','postal_code','longitude','latitude']
        
        widgets = {
            'address':forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring','placeholder':'start typing...'}),
            'country':forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring'}),
            'county':forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring'}),
            'city':forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring'}),
            'postal_code':forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring'}),
            'longitude':forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring', 'readonly':True}),
            'latitude':forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring', 'readonly':True}),
            
            'profile_picture':forms.FileInput(attrs={'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring'}),
            'cover_picture':forms.FileInput(attrs={'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring'}),
            
            
        }
    
        