from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User  # Import the User model



class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User  # Import the User model from django.contrib.auth.models
        fields = ['username', 'email', 'password1', 'password2']
        

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'User Name'
        self.fields['password'].label = 'Password'
