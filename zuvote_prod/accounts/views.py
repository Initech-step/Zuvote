from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ExtendedUserCreationForm, ExtraDataForm, ZuvoteLoginForm, ResetPasswordForm
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ExtraUserData
from django.shortcuts import get_object_or_404
# Create your views here.



def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        form2 = ExtraDataForm(request.POST)

        if form.is_valid() and form2.is_valid():
            print("valid forms")
            users = form.save()

            extra = form2.save(commit=False)
            extra.user = users
            extra.save()
            return redirect('login_zuvote')
        else:
            print('Invalid forms')

    form = ExtendedUserCreationForm(request.POST or None)
    form2 = ExtraDataForm(request.POST or None)
    return render(request, 'accounts/register.html', {'form': form, 'form2': form2})



def login_zuvote(request):
    if request.method == 'POST':
        form = ZuvoteLoginForm(request.POST)

        if form.is_valid():
            nameused = form.cleaned_data['username']
            passwordused = form.cleaned_data['password']

            userdata = authenticate(username=nameused, password=passwordused)

            if userdata is not None:
                login(request, userdata)
                return redirect('panel')
            else:
                messages.add_message(request, messages.INFO, 'Invalid Credentials')
                return redirect('login_zuvote')

        else:
            return HttpResponse('Invalid form')

    form = ZuvoteLoginForm(request.POST or None)
    return render(request, 'accounts/login.html', {'form': form})



def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():

            #get user data
            username_x = form.cleaned_data['username']
            reset_code = form.cleaned_data['reset_code']
            password_a = form.cleaned_data['new_password']
            password_b = form.cleaned_data['confirm_new_password']

            #check our database for such user
            get_hold_of_user = User.objects.get(username=username_x)

            #check our extradata model for such user
            get_reset_code_a = ExtraUserData.objects.get(user=get_hold_of_user)
            #get hold of the reset code
            get_reset_code_b = get_reset_code_a.reset_code

            suggested_reset_code = str(reset_code)
            real_reset_code = str(get_reset_code_b)
            
            if suggested_reset_code == real_reset_code:
                if password_a == password_b:
                    get_hold_of_user.set_password(password_a)
                    get_hold_of_user.save()
                    messages.add_message(request, messages.INFO, 'Password reset successfully, please log in with new details')
                    return redirect('login_zuvote')
                else:
                    messages.add_message(request, messages.INFO, 'Your passwords dont match')
                    return redirect('reset_password')
            else:
                messages.add_message(request, messages.INFO, 'Credentials not found in our records')
                return redirect('reset_password')

        
        else:
            return HttpResponse('Invalid')

    form =  ResetPasswordForm(request.POST or None)
    return render(request, 'accounts/reset_password.html', {'form':form})



def logout_page(request):
    logout(request)
    return redirect('login_zuvote')
    # Redirect to a success page.