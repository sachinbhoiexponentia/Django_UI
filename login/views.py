from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm,RegistrationForm  # Import your custom login form
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in
            return redirect('profile')  # Redirect to a user profile page or another URL
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})







def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']  # Get the "Remember Me" value

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Threshold_Logic_Config_View')  
            else:
                request.session['login_error'] = 'Invalid credentials'
                return redirect('login')  
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = CustomLoginForm()
    return render(request, 'login/login.html', {'form': form})


# for login views
# from django.contrib.auth.decorators import login_required

# @login_required
# def protected_view(request):
#     # Your view logic here