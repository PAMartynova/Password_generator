from django.shortcuts import render, redirect
import random
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

def home(request):
    return render(request, 'generator/home.html')

def password(request):
    digits = '0123456789'
    lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
    uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    punctuation = '!#$%&*+-=?@^_'
    chars = ''
    length = int(request.GET.get('length', 11))
    if request.GET.get('lowercase'):
        chars += lowercase_letters
    if request.GET.get('uppercase'):
        chars += uppercase_letters
    if request.GET.get('numbers'):
        chars += digits
    if request.GET.get('symbols'):
        chars += punctuation
    if chars == '':
        chars += lowercase_letters

    password = ''.join(random.sample(chars, length))

    return render(request, 'generator/password.html', {'password':password})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'generator/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'generator/signupuser.html', {'form':UserCreationForm(), 'error': 'This username has already been taken. Please, choose another one'})
        else:
            return render(request, 'generator/signupuser.html', {'form':UserCreationForm(), 'error': 'Password did not match. Please, try again'})


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'generator/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not user:
            return render(request, 'generator/loginuser.html', {'form':AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')